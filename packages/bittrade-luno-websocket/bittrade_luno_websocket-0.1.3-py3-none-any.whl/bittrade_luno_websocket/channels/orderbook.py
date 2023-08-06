from decimal import Decimal
import functools
import logging
import os
from elm_framework_helpers import schedulers
from elm_framework_helpers.ccxt.models import orderbook as ccxtOrderbook
from elm_framework_helpers.websockets.models import (
    bundle,
    EnhancedWebsocket,
    message_types,
    status,
)
from elm_framework_helpers.websockets.operators import connection_operators
from elm_framework_helpers.operators import retry_with_delay
from typing import Any, Callable, Literal, Optional, TypedDict, cast
from bittrade_luno_websocket.connection import public
from bittrade_luno_websocket.models.orderbook import RawOrderBook, RawOrder
from bittrade_luno_websocket.rest.get_book import load_order_book_http

import reactivex
from reactivex import (
    Observable,
    observable,
    abc,
    operators,
    disposable,
    observer,
    throw,
)
from reactivex.scheduler import ThreadPoolScheduler
from returns import result, maybe

logger = logging.getLogger(__name__)


class DeleteUpdate(TypedDict):
    order_id: str


class CreateUpdate(TypedDict):
    order_id: str
    price: str
    volume: str
    type: Literal["BID", "ASK"]


class TradeUpdate(TypedDict):
    order_id: str
    base: str
    counter: str
    maker_order_id: str
    taker_order_id: str


def handle_create_update(
    book: RawOrderBook, create_update: CreateUpdate
) -> result.Success[RawOrderBook]:
    is_ask = create_update["type"] == "ASK"
    key = "asks" if is_ask else "bids"
    relevant_list = list(book[key])
    # Find where it belongs
    new_order_price = float(create_update["price"])
    for index, order in enumerate(relevant_list):
        if is_ask and float(order["price"]) > new_order_price:
            break
        if not is_ask and float(order["price"]) < new_order_price:
            break
    else:
        index = len(relevant_list)
    relevant_list.insert(
        index,
        {
            "id": create_update["order_id"],
            "price": create_update["price"],
            "volume": create_update["volume"],
        },
    )
    book[key] = relevant_list
    return result.Success(book)


def handle_delete_update(book: RawOrderBook, delete_update: DeleteUpdate):
    # To avoid duplicate loops, check length
    old_asks_length = len(book["asks"])
    book["asks"] = [
        ask for ask in book["asks"] if ask["id"] != delete_update["order_id"]
    ]
    if old_asks_length == len(book["asks"]):
        old_bids_length = len(book["bids"])
        # was not removed from there, remove from bids
        book["bids"] = [
            bid for bid in book["bids"] if bid["id"] != delete_update["order_id"]
        ]
        if old_bids_length == len(book["bids"]):
            # Did not delete from anywhere? Should be an error
            return result.Failure("Delete item not found")
    # Deletes are single items so we can return here
    return result.Success(book)


def handle_trade_updates(book: RawOrderBook, trade_updates: list[TradeUpdate]):
    for update in trade_updates:
        for order in book["asks"] + book["bids"]:
            if order["id"] == update["order_id"]:
                # Update volume
                new_volume = Decimal(order["volume"]) - Decimal(update["base"])
                order["volume"] = str(new_volume)
                break
        else:
            return result.Failure("Trade update item not found")

    # Deletes are single items so we can return here
    return result.Success(book)


def handle_empty_book(message: dict):
    if "asks" in message:
        # Snapshots contain asks and bids
        return result.Success(cast(RawOrderBook, message))
    return result.Failure("No book and not a snapshot")


def handle_update(book: RawOrderBook, message: dict):
    book = book.copy()
    book["timestamp"] = message["timestamp"]
    outcome = None
    if delete_update := message.get("delete_update"):
        outcome = handle_delete_update(book, delete_update)
    if create_update := cast(CreateUpdate, message.get("create_update")):
        outcome = handle_create_update(book, create_update)
    if trade_updates := cast(list[TradeUpdate], message.get("trade_updates")):
        outcome = handle_trade_updates(book, trade_updates)
    if not outcome:
        return result.Failure("No update type found")

    return outcome


def handle_orderbook_message(
    book: maybe.Maybe[RawOrderBook], message: dict
) -> result.Result[RawOrderBook, str]:
    outcome = book.map(lambda b: handle_update(b, message)).or_else_call(
        lambda: (handle_empty_book(message))
    )
    return outcome


def log_error(x: str):
    logger.error("Error in orderbook process: %s", x)
    return x


SEQUENCE_ERROR = "SEQUENCE"


def message_received(
    message: bundle.WebsocketBundle, last_sequence: int, book: maybe.Maybe[RawOrderBook]
) -> result.Result[RawOrderBook, str]:
    socket, message_type, content = message
    del socket  # unused
    if message_type == message_types.WEBSOCKET_STATUS:
        if (
            content == status.WEBSOCKET_CLOSED
        ):  # there should be no other status getting to this point
            # On closed, emit a Nothing
            return result.Failure("Socket closed")
        return result.Failure(f"Only closed status should be received; got {content}")

    elif message_type == message_types.WEBSOCKET_MESSAGE:
        content = cast(dict, content)
        # Check sequence
        new_sequence = int(content["sequence"])
        if last_sequence and not new_sequence == last_sequence + 1:
            # Since we use a serializable disposable, setting it anew will dispose of the old sub, aka disconnect the socket
            return result.Failure(SEQUENCE_ERROR)
        else:
            return handle_orderbook_message(book, content)
    return result.Failure(
        f"Only status and message should be received; got {message_type}"
    )


def books_differ(valid_book: RawOrderBook, computed_book: RawOrderBook):
    """Note: this returns True if books are different"""
    for valid_entry, computed_entry in zip(
        valid_book["asks"][:100] + valid_book["bids"][:100],
        computed_book["asks"][:100] + computed_book["bids"][:100],
    ):
        if (
            Decimal(valid_entry["volume"]) != Decimal(computed_entry["volume"])
            or valid_entry["price"] != computed_entry["price"]
        ):
            return True
    return False


def find_corresponding_timestamped_book_operator(
    books: list[RawOrderBook], valid_book_timestamp: int
):
    return reactivex.of(*books).pipe(
        operators.start_with(None),
        operators.pairwise(),
        operators.filter(
            lambda x: x[0]
            and x[1]
            and x[0]["timestamp"] <= valid_book_timestamp
            and x[1]["timestamp"] >= valid_book_timestamp
        ),
        operators.map(lambda x: x[0]),
    )


def emit_invalid_orderbook(
    data: tuple[RawOrderBook, list[RawOrderBook]]
) -> Observable[Any]:
    valid_book, books = data
    # Find the book corresponding to this timestamp
    valid_book_timestamp = valid_book["timestamp"]
    return find_corresponding_timestamped_book_operator(
        books, valid_book_timestamp
    ).pipe(
        operators.filter(lambda computed_book: books_differ(valid_book, computed_book)),
    )


def filter_valid_orderbook(
    book: Observable[maybe.Maybe[RawOrderBook]], load_book: Observable[RawOrderBook]
) -> Callable[[int], Observable[bool]]:
    def _filter_valid_orderbook(timestamp: int) -> Observable[bool]:
        # Start recording the books
        return load_book.pipe(
            operators.with_latest_from(
                book.pipe(
                    operators.reduce(
                        lambda acc, current: acc + [current],
                        cast(list[RawOrderBook], []),
                    )
                )
            ),
            operators.flat_map(emit_invalid_orderbook),
        )

    return _filter_valid_orderbook


def subscribe_to_orderbook(symbol: str):
    book: maybe.Maybe[RawOrderBook] = maybe.Nothing
    last_sequence: int = 0

    def reset_sequence(err, socket):
        nonlocal last_sequence
        logger.error("Error in orderbook process: %s", err)
        if err == SEQUENCE_ERROR:
            try:
                socket.socket.close()
            except Exception as e:
                logger.error("Error closing socket: %s", e)

        last_sequence = 0
        return cast(maybe.Maybe[RawOrderBook], maybe.Nothing)

    def set_book(new_book: maybe.Maybe[RawOrderBook], content: dict):
        nonlocal book, last_sequence
        book = new_book
        # TODO use railway pattern
        if book:
            last_sequence = int(content["sequence"])
        return book

    def _subscribe_to_orderbook(
        source: observable.Observable[bundle.WebsocketBundle],
    ) -> observable.Observable[maybe.Maybe[RawOrderBook]]:
        def subscribe(
            observer: abc.ObserverBase, scheduler: abc.SchedulerBase | None = None
        ):
            def map_to_book(x: bundle.WebsocketBundle):
                socket, message_type, content = x
                return (
                    message_received(x, last_sequence, book)
                    .map(lambda x: maybe.Some(x))
                    .lash(lambda err: reset_sequence(err, socket))
                    .map(lambda book: (set_book(book, content)))
                )

            book_observable = source.pipe(
                operators.map(map_to_book), operators.replay(1)
            )

            # Keep a single connection
            sub = disposable.SerialDisposable()
            if type(scheduler) is ThreadPoolScheduler:
                raise Exception(
                    "Cannot use ThreadPoolScheduler for orderbook as it may lead to invalid book; use single thread"
                )
            sub.set_disposable(book_observable.connect(scheduler=scheduler))
            # Watch book observable for errors
            reactivex.timer(60, 180, scheduler=scheduler).pipe(
                filter_valid_orderbook(book_observable, load_order_book(symbol)),
            ).subscribe(
                on_next=lambda _: (
                    sub.set_disposable(book_observable.connect(scheduler=scheduler))
                )
            )

            return disposable.CompositeDisposable(
                sub, book_observable.subscribe(observer, scheduler=scheduler)
            )

        return observable.Observable(subscribe)

    return _subscribe_to_orderbook


def keep_messages_and_disconnects(x: bundle.WebsocketBundle):
    """
    A reactivex operator that filters a stream of `bundle.WebsocketBundle` objects,
    keeping only those that contain a message or a closed websocket status update.

    Args:
        x: A `bundle.WebsocketBundle` object containing a websocket object, message, and status update.

    Returns:
        A boolean indicating whether the message or status update should be kept.

    Examples:
        >>> bundle1 = (websocket1, message1, status_update1)
        >>> bundle2 = (websocket2, message2, status_update2)
        >>> source = reactivex.from_iterable([bundle1, bundle2])
        >>> operator = keep_messages_and_disconnects
        >>> observer = TestObserver()
        >>> disposable = operator(source).subscribe(observer)
        >>> observer.assert_values(bundle1, bundle2)
    """
    return x[1] == message_types.WEBSOCKET_MESSAGE or (
        x[1] == message_types.WEBSOCKET_STATUS and x[2] == status.WEBSOCKET_CLOSED
    )


def orderbook_connection(
    api_key: str, secret: str, symbol: str, stable_delay: int = 10
) -> observable.Observable[maybe.Maybe[RawOrderBook]]:
    """Connects to the orderbook websocket and returns an observable that emits the orderbook.

    Args:
        api_key (str): Api key
        secret (str): Api secret
        symbol (str): Symbol to subscribe to
        stable_delay (int, optional): How long without an error before we consider connection to be stable. Defaults to 10.

    Returns:
        observable.Observable[maybe.Maybe[OrderBook]]: An observable that emits the orderbook.
    """
    raise NotImplementedError("This function is not fully implemented yet")
    return public.public_connection(api_key, secret, orderbook_symbol=symbol).pipe(
        operators.filter(keep_messages_and_disconnects), subscribe_to_orderbook(symbol)
    )


def on_orderbook_error(err: str, _src):
    logger.error("Error in orderbook load: %s", err)
    delay = 0.25
    if err == "ErrTooManyRequests":
        delay = 2
    return reactivex.timer(delay).pipe(operators.ignore_elements())


def top_orderbook_connection(symbol: str, frequency: float = 0.3):
    scheduler = ThreadPoolScheduler(max_workers=int(60 / frequency))
    return reactivex.timer(0, frequency).pipe(
        operators.flat_map(lambda _: load_order_book_http(symbol)),
        operators.catch(on_orderbook_error),
        operators.repeat(),
        operators.subscribe_on(scheduler),
    )
