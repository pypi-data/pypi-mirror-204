# screening.py

import os
import time
import asyncio
import warnings
from abc import ABCMeta, abstractmethod
import datetime as dt
import threading
from typing import (
    Optional, Union, Dict, Iterable,
    Any, Protocol, List, Type, Tuple
)

import pandas as pd
import numpy as np
import ccxt
import ccxt.pro as ccxtpro

from represent import BaseModel, Modifiers

from auto_screener.hints import Number
from auto_screener.dataset import (
    OPEN, HIGH, LOW, CLOSE, VOLUME, BIDS,
    ASKS, row_to_dataset, DATE_TIME, OHLCV_COLUMNS
)
from auto_screener.base import terminate_thread
from auto_screener.tickers import parts_to_ticker
from auto_screener.interval import interval_to_total_time
from auto_screener.dataset import save_dataset, load_dataset

__all__ = [
    "AutoDataset",
    "AutoScreener",
    "wait_for_update",
    "wait_for_initialization",
    "WaitingState",
    "configure_exchange",
    "validate_ticker",
    "is_valid_ticker",
    "is_valid_source",
    "AutoDataCollector",
    "ohlcv_to_dataset",
    "MultiScreener",
    "collect_exchanges",
    "collect_assets",
    "collect_mutual_assets",
    "collect_tickers",
    "collect_mutual_tickers"
]

def ohlcv_to_dataset(data: Iterable[Iterable]) -> pd.DataFrame:
    """
    Adjusts the dataset to an asset Open, High, Low, Close, Bids, Asks, Volume dataset.

    :param data: The data to adjust.

    :return: The asset dataset.
    """

    data = pd.DataFrame(data)

    index_column_name = list(data.columns)[0]

    data.index = pd.to_datetime(data[index_column_name], unit="ms")
    del data[index_column_name]
    data.index.name = DATE_TIME
    data.columns = list(OHLCV_COLUMNS)

    return data
# end ohlcv_to_dataset

class WaitingState(BaseModel):
    """A class to represent the waiting state of screener objects."""

    modifiers = Modifiers(excluded=["screeners"])

    def __init__(self, screeners: Iterable, delay: Number, count: int) -> None:
        """
        Defines the class attributes.

        :param screeners: The screener objects.
        :param delay: The waiting delay.
        :param count: The iterations count.
        """

        self.screeners: Iterable[AutoDataCollector] = screeners

        self.delay = delay
        self.count = count

        self.time = dt.timedelta(seconds=self.delay * self.count)
    # end __init__
# end WaitingState

class AutoDataCollector(Protocol, metaclass=ABCMeta):
    """A class to represent an abstract parent class of data collectors."""

    market: pd.DataFrame

    ticker: str
    source: str

    screening_process: Optional[threading.Thread]
    timeout_process: Optional[threading.Thread]

    running: bool
    block: bool

    TICKERS: Dict[str, List[str]]

    def validate_ticker(self, ticker: Any) -> str:
        """
        Validates the ticker value.

        :param ticker: The name of the ticker.

        :return: The validates ticker.
        """

        if not hasattr(self, "source"):
            raise AttributeError(
                f"Source attribute must be defined before "
                f"attempting to validate the ticker attribute."
            )
        # end if

        return validate_ticker(self.source, ticker, screener=self)
    # end validate_ticker

    def wait_for_initialization(
            self,
            delay: Optional[Union[Number, dt.timedelta]] = None,
            once: Optional[bool] = False,
            stop: Optional[Union[bool, int]] = False
    ) -> WaitingState:
        """
        Waits for all the screeners to update.

        :param delay: The delay for the waiting.
        :param once: The value to get data only once.
        :param stop: The value to stop the screener objects.

        :returns: The total delay.
        """

        return wait_for_initialization(
            self, delay=delay, once=once, stop=stop
        )
    # end wait_for_initialization

    def wait_for_update(
            self,
            delay: Optional[Union[Number, dt.timedelta]] = None,
            once: Optional[bool] = False,
            stop: Optional[Union[bool, int]] = False
    ) -> WaitingState:
        """
        Waits for all the screeners to update.

        :param delay: The delay for the waiting.
        :param once: The value to get data only once.
        :param stop: The value to stop the screener objects.

        :returns: The total delay.
        """

        return wait_for_update(
            self, delay=delay, once=once, stop=stop
        )
    # end wait_for_update

    def blocking(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self.block
    # end blocking

    @abstractmethod
    def run_loop(self) -> None:
        """Runs the process of the price screening."""

    def run(
            self,
            wait: Optional[Union[bool, Number, dt.timedelta, dt.datetime]] = False,
            block: Optional[bool] = False,
            timeout: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> threading.Thread:
        """
        Runs the process of the price screening.

        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param timeout: The valur to add a timeout to the process.
        """

        self.screening_process = threading.Thread(target=self.run_loop)

        self.screening_process.start()

        if timeout:
            self.timeout(timeout)
        # end if

        if block:
            self.block = block

            while self.blocking():
                pass
            # end while
        # end if

        if isinstance(wait, dt.datetime):
            wait = wait - dt.datetime.now()
        # end if

        if isinstance(wait, dt.timedelta):
            wait = wait.total_seconds()
        # end if

        if isinstance(wait, bool) and wait:
            self.wait_for_initialization()

        elif isinstance(wait, (int, float)):
            time.sleep(wait)
        # end if

        return self.screening_process
    # end run

    def timeout(
            self, duration: Union[Number, dt.timedelta, dt.datetime]
    ) -> threading.Thread:
        """
        Runs a timeout for the process.

        :param duration: The duration of the timeout.

        :return: The timeout process.
        """

        if isinstance(duration, dt.datetime):
            duration = duration - dt.datetime.now()
        # end if

        if isinstance(duration, dt.timedelta):
            duration = duration.total_seconds()
        # end if

        self.timeout_process = threading.Thread(
            target=lambda: (time.sleep(duration), self.terminate())
        )

        self.timeout_process.start()

        return self.timeout_process
    # end timeout

    def terminate(self) -> None:
        """Stops the trading process."""

        self.stop()
    # end terminate

    def stop(self) -> None:
        """Stops the screening process."""

        self.running = False

        terminate_thread(self.screening_process)
    # end stop
# end AutoDataCollector

def is_valid_source(
        source: str,
        screener: Optional[
            Union[AutoDataCollector, Type[AutoDataCollector]]
        ] = None
) -> bool:
    """
    checks of the source os a valid exchange name.

    :param source: The source name to validate.
    :param screener: The screener object for the exchanges.

    :return: The validation value.
    """

    return source in (screener or AutoScreener).TICKERS
# end is_valid_source

def configure_exchange(
        source: str,
        pro: Optional[bool] = True,
        screener: Optional[
            Union[AutoDataCollector, Type[AutoDataCollector]]
        ] = None,
        options: Optional[Dict[str, Any]] = None
):
    """
    Validates the exchange source value.

    :param source: The name of the exchange platform.
    :param screener: The screener object for the exchanges.
    :param pro: The value for the pro interface.
    :param options: The ccxt options.

    :return: The validates source.
    """

    screener = screener or AutoScreener

    if source not in screener.exchanges:
        try:
            exchange = getattr(
                (ccxtpro if pro else ccxt), source
            )(options)

        except AttributeError:
            raise ValueError(f"Unrecognized exchange name: {source}.")
        # end try

        if not (
            hasattr(exchange, "watch_tickers") or
            hasattr(exchange, "fetch_tickers")
        ):
            raise ValueError(f"Cannot extract data from {source}.")
        # end if

        if not screener.TICKERS.setdefault(source, []):
            try:
                screener.TICKERS[source] = list(
                    getattr(ccxt, source)().load_markets().keys()
                )

            except Exception as e:
                raise ValueError(
                    f"Cannot fetch tickers from {source}. {e}"
                )
            # end try
        # end if

        screener.exchanges[source] = exchange
    # end if

    return screener.exchanges[source]
# end configure_exchange

def is_valid_ticker(
        source: str,
        ticker: str,
        screener: Optional[
            Union[AutoDataCollector, Type[AutoDataCollector]]
        ] = None
) -> bool:
    """
    Returns a value for the ticker being valid for the source exchange.

    :param source: The name of the exchange platform.
    :param ticker: The ticker of the assets.
    :param screener: The screener object for the exchanges.

    :return: The validation-value.
    """

    return ticker in (screener or AutoScreener).TICKERS[source]
# end is_valid_ticker

def validate_ticker(
        source: str,
        ticker: str,
        screener: Optional[
            Union[AutoDataCollector, Type[AutoDataCollector]]
        ] = None
) -> str:
    """
    Validates the ticker value.

    :param source: The name of the exchange platform.
    :param ticker: The name of the ticker.
    :param screener: The screener object for the exchanges.

    :return: The validates ticker.
    """

    if not is_valid_ticker(source, ticker, screener=screener):
        raise ValueError(
            f"ticker {ticker} is not a valid "
            f"ticker for the {source} exchange."
        )
    # end if

    return ticker
# end validate_ticker

class AutoScreener(BaseModel, AutoDataCollector):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - ticker:
        The ticker symbol of an asset to screen.

    - source:
        The name of the exchange platform to screen data from.

    - delay:
        The delay to wait between each data fetching.

    >>> from auto_screener.screening import (
    >>>     AutoScreener, wait_for_initialization
    >>> )
    >>>
    >>> screener = AutoScreener(
    >>>     ticker="BTC-USD", source="binance"
    >>> )
    >>>
    >>> screener.run(wait=True)
    >>>
    >>> while True:
    >>>     print(screener.market.iloc[-1])
    >>>
    >>>     wait_for_update(screener, delay=1)
    """

    modifiers = Modifiers(
        excluded=[
            "market", "exchange", "screening_process",
            "task", 'timeout_process'
        ]
    )

    ASKS = ASKS
    BIDS = BIDS

    DELAY = 0.0

    exchanges = {}

    TICKERS = {
        exchange: []
        for exchange in ccxtpro.exchanges
    }

    COLUMNS = (
        OPEN, HIGH, LOW, CLOSE,
        ASKS, BIDS, VOLUME
    )

    def __init__(
            self,
            ticker: str,
            source: str,
            pro: Optional[bool] = True,
            delay: Optional[Union[Number, dt.timedelta]] = None,
            options: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param ticker: The ticker of the asset.
        :param source: The exchange to get source data from.
        :param delay: The delay for the process.
        :param pro: The value for the pro interface.
        :param options: The ccxt options.
        """

        self.options = options or {}

        self.exchange = configure_exchange(
            source=source, pro=pro, options=self.options
        )

        self.delay = delay or self.DELAY

        self.pro = pro

        self.source = source

        self.ticker = self.validate_ticker(ticker=ticker)

        self.running = False
        self.block = False

        self.market = pd.DataFrame(
            {column: [] for column in self.COLUMNS}, index=[]
        )

        self.market.index.name = DATE_TIME

        self.screening_process = None
        self.timeout_process = None

        self.task = None
    # end __init__

    def __getstate__(self) -> Dict[str, Any]:
        """
        Returns the data of the object.

        :return: The state of the object.
        """

        data = self.__dict__.copy()

        data["task"] = None
        data["screening_process"] = None
        data["timeout_process"] = False
        data["exchange"] = None

        return data
    # end __getstate__

    def __setstate__(self, state: Dict[str, Any]) -> Any:
        """
        Sets the state of the object.

        :param state: The state to set to the object.
        """

        self.__dict__.update(state)

        self.exchange = configure_exchange(
            source=self.source, pro=self.pro
        )
    # end __setstate__

    async def async_get_market(self) -> Dict[str, Number]:
        """
        Gets the market data.

        :return: The bids and asks.
        """

        if hasattr(self.exchange, "fetch_tickers"):
            method = self.exchange.fetch_tickers

        elif hasattr(self.exchange, "watch_tickers"):
            method = self.exchange.watch_tickers

        else:
            raise AttributeError(
                f"Exchange attribute {self.exchange} of "
                f"{self} must has at least one of the "
                f"methods 'fetch_tickers', or 'watch_tickers'."
            )
        # end if

        if isinstance(self.exchange, getattr(ccxtpro, self.source)):
            data = await method(symbols=[self.ticker])

        elif isinstance(self.exchange, getattr(ccxt, self.source)):
            data = method(symbols=[self.ticker])

        else:
            raise TypeError(
                f"Exchange object {self.exchange} of "
                f"{self} must be from ccxt."
            )
        # end if

        ticker = list(data.keys())[0]

        data[ticker][VOLUME.lower()] = data[ticker]["quoteVolume"]
        data[ticker][self.ASKS.lower()] = data[ticker]["ask"]
        data[ticker][self.BIDS.lower()] = data[ticker]["bid"]

        return {
            key: data[ticker][key.lower()] for key in
            self.COLUMNS
        }
    # end async_get_market

    async def get_market(self) -> Dict[str, Number]:
        """
        Gets the market data.

        :return: The bids and asks.
        """

        task = self.async_get_market()

        try:
            loop = asyncio.get_event_loop()

            self.task = loop.create_task(task)

            return await self.task

        except RuntimeError:
            return asyncio.run(task)
        # end try
    # end get_market

    async def async_run_loop(self) -> None:
        """Runs the processes of price screening."""

        self.running = True

        delay = self.delay

        if isinstance(delay, dt.timedelta):
            delay = delay.total_seconds()
        # end if

        while self.running:
            start = time.time()

            try:
                data = await self.async_get_market()

            except Exception as e:
                self.terminate()

                raise RuntimeError(
                    f"Could not complete task. {str(e)}"
                ) from e
            # end try

            new_data = pd.DataFrame(
                data, index=pd.to_datetime(
                    [int(time.time() * 1000)], unit="ms"
                )
            )
            new_data.index.name = DATE_TIME

            self.market = pd.concat([self.market, new_data])
            self.market.index.name = DATE_TIME

            end = time.time()

            if delay:
                time.sleep(max([delay - (end - start), 0]))
            # end if
        # end while
    # end async_run

    async def async_run(self) -> None:
        """Runs the processes of price screening."""

        task = self.async_run_loop()

        try:
            loop = asyncio.get_event_loop()

            self.task = loop.create_task(task)

            await self.task

        except RuntimeError:
            asyncio.run(task)
        # end try
    # end async_run

    def run_loop(self) -> None:
        """Runs the process of the price screening."""

        asyncio.run(self.async_run())
    # end run_loop

    def stop(self) -> None:
        """Stops the screening process."""

        super().stop()

        if self.task is not None:
            self.task.cancel()
        # end if
    # end stop

    def terminate(self) -> None:
        """Stops the trading process."""

        super().terminate()
    # end terminate
# end Screener

class AutoDataset(BaseModel, AutoDataCollector):
    """
    A class to represent a live asset data builder.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    You can also use it to build real time datasets of Open
    High Low Close Volume, with Bids and Asks.

    Parameters:

    - ticker:
        The ticker symbol of an asset to screen.

    - source:
        The name of the exchange platform to screen data from.

    - interval:
        The interval for the time between data points in the dataset.

    - delay:
        The delay to wait between each data fetching.

    - screener:
        The screener object to connect to for creating the dataset.

    - length:
        An initial dataset length to start with.

    >>> from auto_screener.screening import (
    >>>     AutoDataset, wait_for_initialization
    >>> )
    >>> from auto_screener.interval import interval_to_total_time
    >>>
    >>> interval = "1m"
    >>>
    >>> dataset = AutoDataset(
    >>>     ticker="BTC-USD", source="binance", interval=interval
    >>> )
    >>>
    >>> dataset.run(wait=True)
    >>>
    >>> print(dataset.market.iloc[-1].splitlines()[0])
    >>>
    >>> while True:
    >>>     print(dataset.market.iloc[-1].splitlines()[-1])
    >>>
    >>>     wait_for_update(dataset, delay=interval_to_total_time(interval))
    """

    modifiers = Modifiers(
        excluded=[
            "timeout_process", 'market', 'built',
            'exchange', 'screening_process', "delay"
        ]
    )

    screeners: Dict[
        Tuple[str, str, Union[Number, dt.timedelta], bool],
        AutoScreener
    ] = {}

    exchanges = AutoScreener.exchanges

    COLUMNS = AutoScreener.COLUMNS
    TICKERS = AutoScreener.TICKERS

    def __init__(
            self,
            ticker: str,
            source: str,
            interval: str,
            pro: Optional[bool] = True,
            data: Optional[pd.DataFrame] = None,
            length: Optional[Union[bool, int]] = None,
            delay: Optional[Union[Number, dt.timedelta]] = None,
            screener: Optional[AutoScreener] = None,
            options: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param ticker: The ticker of the asset.
        :param source: The exchange to get source data from.
        :param interval: The interval for the data.
        :param data: The base dataset of the asset to add to.
        :param length: The length of the base dataset.
        :param delay: The delay for the process.
        :param screener: The screener object for the dataset.
        :param pro: The value for the pro interface.
        :param options: The ccxt options.
        """

        self.options = options or {}

        self.source = source

        self.interval = interval
        self.ticker = ticker
        self.delay = delay

        self.built = False

        self.pro = pro

        self.screener_key = (
            self.ticker, self.source, self.delay, self.pro
        )

        if self.screener_key not in self.screeners:
            if screener is None:
                self.built = True

                screener = AutoScreener(
                    ticker=self.ticker, source=self.source,
                    delay=self.delay, pro=self.pro,
                    options=self.options
                )
            # end if

            self.screeners[self.screener_key] = screener
        # end if

        self.screener = self.screeners[self.screener_key]

        self.market = self.validate_data(data, length=length)

        ccxt.binance()

        self.exchange = getattr(ccxt, self.source)(self.options)

        self.screening_process = None
        self.timeout_process = None

        self.running = False
        self.block = False
    # end __init__

    def __getstate__(self) -> Dict[str, Any]:
        """
        Returns the data of the object.

        :return: The state of the object.
        """

        data = self.__dict__.copy()

        data["exchange"] = None

        return data
    # end __getstate__

    def __setstate__(self, state: Dict[str, Any]) -> Any:
        """
        Sets the state of the object.

        :param state: The state to set to the object.
        """

        self.__dict__.update(state)

        self.exchange = getattr(ccxt, self.source)()
    # end __setstate__

    def validate_data(self, data: Any, length: Optional[int]) -> pd.DataFrame:
        """
        Validates the asset data value.

        :param data: The asset data.
        :param length: The length of the data to add.

        :return: The validates source.
        """

        if not all(
                hasattr(self, name) for name in ["source", "interval"]
        ):
            raise AttributeError(
                "Source and interval attributes must be defined "
                "before attempting to validate the data parameter data."
            )
        # end if

        if (
            (data is None) and
            (
                (length is None) or
                (length == 0) or
                (length is False) or
                (
                    isinstance(length, int) and
                    not (0 < length <= 500)
                )
            )
        ):
            data = pd.DataFrame(
                {column: [] for column in self.COLUMNS},
                index=[]
            )

        elif (data is None) and (isinstance(length, int)):
            if 0 < length <= 500:
                data = self.data_to_dataset(
                    self.exchange.fetch_ohlcv(
                        symbol=self.ticker,
                        timeframe=self.interval,
                        limit=length
                    )
                )

            else:
                raise ValueError(
                    f"Length must be a positive int between "
                    f"1 and 500 when data is not defined, "
                    f"not: {length}."
                )
            # end if
        # end if

        return data
    # end validate_data

    def data_to_dataset(self, data: Iterable[Iterable]) -> pd.DataFrame:
        """
        Adjusts the dataset to an asset Open, High, Low, Close, Bids, Asks, Volume dataset.

        :param data: The data to adjust.

        :return: The asset dataset.
        """

        data = ohlcv_to_dataset(data=data)

        if len(self.screener.market) == 0:
            asks = [np.nan] * len(data)
            bids = [np.nan] * len(data)

        else:
            asks = (
                self.screener.market[AutoScreener.ASKS].iloc
                [-len(data):].values[:]
            )
            bids = (
                self.screener.market[AutoScreener.BIDS].iloc
                [-len(data):].values[:]
            )
        # end if

        data[AutoScreener.ASKS].values[:] = asks
        data[AutoScreener.BIDS].values[:] = bids

        return data[list(self.COLUMNS)]
    # end data_to_dataset

    def run(
            self,
            wait: Optional[Union[bool, Number, dt.timedelta, dt.datetime]] = False,
            block: Optional[bool] = False,
            timeout: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> threading.Thread:
        """
        Runs the process of the price screening.

        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param timeout: The valur to add a timeout to the process.
        """

        if not self.screener.running:
            self.screener.run(wait=True, block=False, timeout=timeout)
        # end if

        return super().run(wait=wait, block=block, timeout=timeout)
    # end run

    def run_loop(self) -> None:
        """Runs the process of the price screening."""

        self.running = True

        delay = interval_to_total_time(self.interval).seconds

        while self.running:
            start = time.time()

            data = row_to_dataset(self.screener.market, index=-1)

            # noinspection PyBroadException
            try:
                prices = self.validate_data(data=None, length=1)
                prices[AutoScreener.BIDS].values[:] = (
                    data[AutoScreener.BIDS].values[:]
                )
                prices[AutoScreener.ASKS].values[:] = (
                    data[AutoScreener.ASKS].values[:]
                )
                data = prices

            except Exception as e:
                warnings.warn(str(e))
            # end try

            end = time.time()

            self.market = pd.concat([self.market, data])
            self.market = self.market[
                ~self.market.index.duplicated(keep='first')
            ]

            time.sleep(max([delay - (end - start), 0]))
        # end while
    # end run_loop

    def terminate(self) -> None:
        """Stops the trading process."""

        super().terminate()

        if self.built:
            self.screener.terminate()
        # end if
    # end terminate

    def stop(self) -> None:
        """Stops the screening process."""

        super().stop()

        if self.built:
            self.screener.stop()
        # end if
    # end stop
# end LiveAssetData

def wait_for_initialization(
        *screeners: AutoDataCollector,
        delay: Optional[Union[Number, dt.timedelta]] = None,
        once: Optional[bool] = False,
        stop: Optional[Union[bool, int]] = False
) -> WaitingState:
    """
    Waits for all the screeners to update.

    :param screeners: The screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param once: The value to get data only once.
    :param stop: The value to stop the screener objects.

    :returns: The total delay.
    """

    if isinstance(delay, dt.timedelta):
        delay = delay.total_seconds()
    # end if

    delay = delay or 0
    count = 0

    screeners = list(screeners)

    while not all(
        len(screener.market) > 0 for screener in screeners
    ):
        count += 1

        if isinstance(delay, (int, float)) and (count > 0):
            time.sleep(delay)
        # end if
    # end while

    if stop and ((stop == count) or once):
        for screener in screeners:
            screener.stop()
        # end for
    # end if

    return WaitingState(
        screeners=screeners, delay=delay, count=count
    )
# end wait_for_initialization

def wait_for_update(
        *screeners: AutoDataCollector,
        delay: Optional[Union[Number, dt.timedelta]] = None,
        once: Optional[bool] = False,
        stop: Optional[Union[bool, int]] = False
) -> WaitingState:
    """
    Waits for all the screeners to update.

    :param screeners: The screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param once: The value to get data only once.
    :param stop: The value to stop the screener objects.

    :returns: The total delay.
    """

    if isinstance(delay, dt.timedelta):
        delay = delay.total_seconds()
    # end if

    delay = delay or 0
    count = 0

    screeners = list(screeners)

    if screeners:
        wait_for_initialization(
            *screeners, delay=delay, once=once
        )

        indexes = [
            screener.market.index[-1]
            for screener in screeners
        ]

        new_indexes = indexes

        while all(
                indexes[i] == new_indexes[i]
                for i in range(len(screeners))
        ):
            count += 1

            new_indexes = [
                screener.market.index[-1]
                for screener in screeners
            ]

            if isinstance(delay, (int, float)) and (count > 0):
                time.sleep(delay)
            # end if
        # end while

        if stop and ((stop == count) or once):
            for screener in screeners:
                screener.stop()
            # end for
        # end if
    # end if

    return WaitingState(
        screeners=screeners, delay=delay, count=count
    )
# end wait_for_update

def _collect_exchange_assets(
        data: Dict[str, List[str]], source: str, exchange: ccxt.Exchange
) -> None:
    """
    Collects the tickers from the exchanges.

    :param source: The name of the exchange.
    :param exchange: The exchange object.
    :param data: The data to collect the assets.

    :return: The data of the exchanges.
    """

    assets = []

    # noinspection PyBroadException
    try:
        for value in exchange.load_markets().values():
            assets.append(value['base'])
        # end for

        data[source] = list(set(assets))

    except Exception:
        data[source] = []
    # end try
# end _collect_exchange_assets

def _collect_exchange_tickers(
        data: Dict[str, List[str]], source: str, exchange: ccxt.Exchange
) -> None:
    """
    Collects the tickers from the exchanges.

    :param source: The name of the exchange.
    :param exchange: The exchange object.
    :param data: The data to collect the assets.

    :return: The data of the exchanges.
    """

    tickers = []

    # noinspection PyBroadException
    try:
        for value in exchange.load_markets().values():
            tickers.append(parts_to_ticker(value['base'], value['quote']))
        # end for

        data[source] = list(set(tickers))

    except Exception:
        data[source] = []
    # end try
# end _collect_exchange_tickers

def collect_assets(exchanges: Optional[Iterable[str]] = None) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.

    :return: The data of the exchanges.
    """

    data = {}
    markets = {}

    count = 0

    for source in (exchanges or ccxt.__dict__):
        if source in ccxt.exchanges:
            exchange = getattr(ccxt, source)()

            if not (
                hasattr(exchange, 'fetch_tickers') or
                hasattr(exchange, 'watch_tickers')
            ):
                count -= 1

                continue
            # end if

            markets[source] = exchange
        # end if
    # end for

    for source, exchange in markets.items():
        threading.Thread(
            target=_collect_exchange_assets,
            kwargs=dict(source=source, exchange=exchange, data=data)
        ).start()
    # end for

    while (len(markets) - count) > len(data):
        pass
    # end while

    return {key: value for key, value in data.items() if value}
# end collect_tickers

def collect_mutual_assets(exchanges: Optional[Iterable[str]] = None) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.

    :return: The data of the exchanges.
    """

    exchanges = collect_assets(exchanges)

    assets = {}

    for source in exchanges:
        for asset in exchanges[source]:
            assets[asset] = assets.setdefault(asset, 0) + 1
        # end for
    # end for

    return {
        source: [
            asset for asset in exchanges[source]
            if assets.get(asset, 0) > 1
        ]
        for source in exchanges
    }
# end collect_mutual_assets

def collect_tickers(exchanges: Optional[Iterable[str]] = None) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.

    :return: The data of the exchanges.
    """

    data = {}
    markets = {}

    count = 0

    for source in (exchanges or ccxt.__dict__):
        if source in ccxt.exchanges:
            exchange = getattr(ccxt, source)()

            if not (
                hasattr(exchange, 'fetch_tickers') or
                hasattr(exchange, 'watch_tickers')
            ):
                count -= 1

                continue
            # end if

            markets[source] = exchange
        # end if
    # end for

    for source, exchange in markets.items():
        threading.Thread(
            target=_collect_exchange_tickers,
            kwargs=dict(source=source, exchange=exchange, data=data)
        ).start()
    # end for

    while (len(markets) - count) > len(data):
        pass
    # end while

    return {key: value for key, value in data.items() if value}
# end collect_tickers

def collect_mutual_tickers(exchanges: Optional[Iterable[str]] = None) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.

    :return: The data of the exchanges.
    """

    exchanges = collect_tickers(exchanges)

    tickers = {}

    for source in exchanges:
        for ticker in exchanges[source]:
            tickers[ticker] = tickers.setdefault(ticker, 0) + 1
        # end for
    # end for

    return {
        source: [
            ticker for ticker in exchanges[source]
            if tickers.get(ticker, 0) > 1
        ]
        for source in exchanges
    }
# end collect_mutual_tickers

def collect_exchanges(
        currencies: Dict[str, List[str]],
        pairs: Dict[str, List[str]],
        excluded: Optional[Dict[str, Iterable[str]]] = None,
) -> Dict[str, List[str]]:
    """
    Collects the exchanges.

    :param pairs: The data of currencies and their traded quote assets.
    :param currencies: The data of exchanges and their traded currencies.
    :param excluded: The data of excluded pairs for each exchange.

    :return: The data of exchanges and their tickers.
    """

    exchanges: Dict[str, List[str]] = {}

    for platform, currencies in currencies.items():
        exchanges[platform] = []

        for currency in currencies:
            for asset in pairs[currency]:
                if (
                    parts_to_ticker(asset, currency) in
                    excluded.get(platform, [])
                ):
                    continue
                # end if

                exchanges[platform].append(
                    parts_to_ticker(asset, currency)
                )
            # end for
        # end for
    # end for

    return exchanges
# end collect_exchanges

class MultiScreener(BaseModel):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - exchanges:
        The data of exchanges and their tickers to screen.

    - interval:
        The interval for the time between data points in the dataset.

    - delay:
        The delay to wait between each data fetching.

    - length:
        An initial dataset length to start with.

    >>> from auto_screener.screening import (
    >>>     MultiScreener, wait_for_initialization
    >>> )
    >>>
    >>> screener = MultiScreener(
    >>>     exchanges={
    >>>         "binance": ["BTC/USDT", "AAVE/EUR"],
    >>>         "bittrex": ["GRT/USD", "BTC/USD"]
    >>>     }
    >>> )
    >>>
    >>> screener.run(wait=True)
    >>>
    >>> while True:
    >>>     screener.wait_for_update(delay=1)
    """

    modifiers = Modifiers(
        excluded=[
            "exchange", "screening_process",
            "timeout_process", "screeners"
        ]
    )

    LOCATION = "datasets"
    INTERVAL = "1m"

    DELAY = 1

    def __init__(
            self,
            exchanges: Dict[str, Iterable[str]],
            delay: Optional[Union[Number, dt.timedelta]] = None,
            interval: Optional[Union[bool, str]] = None,
            length: Optional[Union[int, bool]] = None,
            location: Optional[str] = None,
            pro: Optional[bool] = False,
            options: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param interval: The interval of the data to load.
        :param exchanges: The data of exchanges and their tickers.
        :param pro: The value to use the pro interface.
        :param location: The saving location for the data.
        :param delay: The delay between each data fetching request.
        :param length: The length of the data to get in each request.
        :param options: The ccxt options.
        """

        if isinstance(interval, bool) and interval:
            interval = self.INTERVAL

        elif isinstance(interval, bool):
            interval = None
        # end if

        self.options = options or {}

        self.interval = interval
        self.location = location or self.LOCATION

        self.delay = delay or self.DELAY
        self.length = length

        self.pro = pro

        self.exchanges = self.validate_exchanges(exchanges)

        self.running = False
        self.block = False
        self.saving = False

        self.market: Dict[str, Dict[str, Optional[AutoDataCollector]]] = {}
        self.invalid: Dict[str, List[str]] = {}
        self.screeners: List[AutoDataCollector] = []

        self.saving_process = None
        self.timeout_process = None
    # end Screener

    @staticmethod
    def validate_exchanges(data: Any) -> Dict[str, List[str]]:
        """
        Validates the data.

        :param data: The data to validate.

        :return: The valid data.
        """

        if data is None:
            return {}
        # end if

        try:
            if not isinstance(data, dict):
                raise ValueError
            # end if

            new_data = {}

            for key, values in data.items():
                values = list(values)

                if not (
                    isinstance(key, str) and
                    all(isinstance(value, str) for value in values)
                ):
                    raise ValueError
                # end if

                new_data[key] = values
            # end for

        except (TypeError, ValueError):
            raise ValueError(
                f"Exchanges data must be a dictionary of "
                f"exchange names as keys and iterables of "
                f"ticker names as values, not {data}."
            )
        # end try

        return new_data
    # end validate_data

    @staticmethod
    def dataset_path(screener: AutoDataCollector, location: Optional[str] = None) -> str:
        """
        Creates the path to the saving file for the screener object.

        :param screener: The screener object.
        :param location: The saving location of the dataset.

        :return: The saving path for the dataset.
        """

        return (location + "/" if isinstance(location, str) else "") + (
            f"{screener.source}/{screener.ticker.replace('/', '-')}.csv"
        )
    # end dataset_path

    def create_screener(
            self,
            container: Dict[str, Optional[AutoDataCollector]],
            ticker: str,
            source: str
    ) -> None:
        """
        Creates the screener and inserts it into the container.

        :param container: The container to contain the new screener.
        :param ticker: The ticker of the screener.
        :param source: The source of the data.
        """

        try:
            if isinstance(self.interval, str):
                container[ticker] = AutoDataset(
                    ticker=ticker, source=source, options=self.options,
                    interval=self.interval, pro=self.pro, delay=self.delay
                )

            else:
                container[ticker] = AutoScreener(
                    ticker=ticker, source=source, options=self.options,
                    pro=self.pro, delay=self.delay
                )
            # end if

        except ValueError:
            container[ticker] = None

            self.invalid.setdefault(source, []).append(ticker)
        # end try
    # end create_screener

    @staticmethod
    def configure_screener_dataset(
            screener: AutoDataCollector, path: str, length: Optional[int] = None
    ) -> None:
        """
        Configures the dataset of the screener.

        :param screener: The screener object to configure the dataset for.
        :param path: The saving or loading path for the dataset.
        :param length: The length of the dataset to fetch.
        """

        if os.path.exists(path):
            try:
                screener.market = load_dataset(path=path)

            except Exception as e:
                warnings.warn(str(e))
            # end try

        else:
            if isinstance(screener, AutoDataset):
                screener.market = screener.validate_data(
                    data=None, length=length
                )
            # end if

            if len(screener.market) > 0:
                save_dataset(dataset=screener.market, path=path)
            # end if
        # end if
    # end configure_screener_dataset

    def wait_for_initialization(
            self,
            delay: Optional[Union[Number, dt.timedelta]] = None,
            once: Optional[bool] = False,
            stop: Optional[Union[bool, int]] = False
    ) -> WaitingState:
        """
        Waits for all the screeners to update.

        :param delay: The delay for the waiting.
        :param once: The value to get data only once.
        :param stop: The value to stop the screener objects.

        :returns: The total delay.
        """

        return wait_for_initialization(
            *[
                screener.screener
                if isinstance(screener, AutoDataset)
                else screener
                for screener in self.screeners
            ], delay=delay, once=once, stop=stop
        )
    # end wait_for_initialization

    def wait_for_update(
            self,
            delay: Optional[Union[Number, dt.timedelta]] = None,
            once: Optional[bool] = False,
            stop: Optional[Union[bool, int]] = False
    ) -> WaitingState:
        """
        Waits for all the screeners to update.

        :param delay: The delay for the waiting.
        :param once: The value to get data only once.
        :param stop: The value to stop the screener objects.

        :returns: The total delay.
        """

        return wait_for_update(
            *self.screeners, delay=delay, once=once, stop=stop
        )
    # end wait_for_update

    def initialize_screeners(self) -> None:
        """Initializes the screeners."""

        self.market.clear()

        for exchange, tickers in self.exchanges.items():
            self.market[exchange] = {}

            for ticker in tickers:
                threading.Thread(
                    target=self.create_screener,
                    kwargs=dict(
                        container=self.market[exchange],
                        ticker=ticker, source=exchange
                    )
                ).start()
            # end for
        # end for

        while (
            sum(len(screeners) for screeners in self.market.values()) <
            sum(len(tickers) for tickers in self.exchanges.values())
        ):
            time.sleep(3)
        # end while

        self.screeners.clear()

        for exchange in self.market.values():
            for ticker, screener in exchange.copy().items():
                if isinstance(screener, (AutoScreener, AutoDataset)):
                    self.screeners.append(screener)

                else:
                    exchange.pop(ticker)
                # end if
            # end for
        # end for
    # end initialize_screeners

    def prepare_screeners(self) -> None:
        """Initializes the screeners."""

        if not (self.market and self.screeners):
            self.initialize_screeners()
        # end if

        for screener in self.screeners:
            path = self.dataset_path(
                screener=screener, location=self.location
            )

            threading.Thread(
                target=self.configure_screener_dataset,
                kwargs=dict(
                    screener=screener, path=path,
                    length=self.length
                )
            ).start()
        # end for
    # end prepare_screeners

    def start_screeners(
            self,
            wait: Optional[Union[bool, Number, dt.timedelta, dt.datetime]] = False,
            timeout: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> None:
        """
        Runs the data collection.

        :param timeout: The valur to add a timeout to the process.
        :param wait: The value to wait after starting to run the process.
        """

        self.prepare_screeners()

        for screener in self.screeners:
            threading.Thread(
                target=screener.run,
                kwargs=dict(
                    timeout=timeout, wait=False, block=False
                )
            ).start()
        # end for

        if isinstance(wait, dt.datetime):
            wait = wait - dt.datetime.now()
        # end if

        if isinstance(wait, dt.timedelta):
            wait = wait.total_seconds()
        # end if

        if isinstance(wait, bool) and wait:
            self.wait_for_initialization()

        elif isinstance(wait, (int, float)):
            time.sleep(wait)
        # end if
    # end start_screeners

    def stop(self) -> None:
        """Stops the screening process."""

        self.saving = False

        terminate_thread(self.saving_process)
    # end stop

    def terminate(self) -> None:
        """Stops the screening process."""

        self.running = False

        self.stop()

        for screener in self.screeners:
            screener.terminate()
        # end for
    # end terminate

    def blocking(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self.block
    # end blocking

    def save_dataset(self, screener: AutoDataCollector) -> None:
        """
        Saves the data of the screener.

        :param screener: The screener object to save its data.
        """

        save_dataset(
            dataset=screener.market,
            path=self.dataset_path(
                screener=screener, location=self.location
            )
        )
    # end save_dataset

    def run_loop(self) -> None:
        """Runs the process of the price screening."""

        self.running = True

        while self.running:
            for screener in self.screeners:
                self.save_dataset(screener=screener)
            # end for

            delay = self.delay

            if isinstance(self.delay, dt.timedelta):
                delay = delay.total_seconds()
            # end if

            time.sleep(delay or 1)
        # end while
    # end run_loop

    def timeout(
            self, duration: Union[Number, dt.timedelta, dt.datetime]
    ) -> threading.Thread:
        """
        Runs a timeout for the process.

        :param duration: The duration of the timeout.

        :return: The timeout process.
        """

        if isinstance(duration, dt.datetime):
            duration = duration - dt.datetime.now()
        # end if

        if isinstance(duration, dt.timedelta):
            duration = duration.total_seconds()
        # end if

        self.timeout_process = threading.Thread(
            target=lambda: (time.sleep(duration), self.stop())
        )

        self.timeout_process.start()

        return self.timeout_process
    # end timeout

    def run(
            self,
            save: Optional[bool] = True,
            block: Optional[bool] = False,
            wait: Optional[Union[bool, Number, dt.timedelta, dt.datetime]] = False,
            timeout: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> Optional[threading.Thread]:
        """
        Runs the process of the price screening.

        :param save: The value to save the data.
        :param block: The value to block the execution.
        :param timeout: The valur to add a timeout to the process.
        :param wait: The value to wait after starting to run the process.
        """

        self.start_screeners(timeout=timeout, wait=wait)

        if save:
            self.saving = True

            self.saving_process = threading.Thread(
                target=self.run_loop
            )

            self.saving_process.start()
        # end if

        if timeout:
            self.timeout(timeout)
        # end if

        if block:
            self.block = block

            while self.blocking() and self.running:
                pass
            # end while
        # end if

        if save:
            return self.saving_process
        # end if
    # end run
# end Screener