import time
from datetime import datetime
from typing import Any, Dict, Mapping, Optional
from urllib.parse import urlencode

import numpy as np
import pandas as pd
from requests import Request, Session

from novalabs.interfaces.client_interface import ClientInterface
from novalabs.utils.constant import DATA_FORMATING
from novalabs.utils.helpers import interval_to_milliseconds


class BTCEX(ClientInterface):
    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        passphrase: str = "",
        limit: int = 2000,
    ):
        super().__init__(
            api_key=api_key, api_secret=api_secret, passphrase=passphrase, limit=limit
        )

        self.based_endpoint = "https://api.btcex.com/api/v1"
        self._session = Session()

        self.access_token: str = ""
        self.refresh_token: str = ""
        self.end_connection_date: float = np.Inf
        self.connected: bool = False
        if api_key != "" and api_secret != "":
            self._connect("client_credentials")

    # API REQUEST FORMAT
    def _send_request(
        self,
        end_point: str,
        request_type: str,
        params: Optional[Mapping[str, Any]] = {},
        signed: bool = False,
    ) -> dict:
        if self.connected and self.end_connection_date - time.time() < 86400:
            self.connected = False
            self._connect("refresh_token")

        if params is None:
            params = {}

        if request_type == "POST":
            request = Request(
                request_type, f"{self.based_endpoint}{end_point}", json=params
            )
        elif request_type == "GET":
            request = Request(
                request_type,
                f"{self.based_endpoint}{end_point}",
                params=urlencode(params, True),
            )
        else:
            raise ValueError("Please enter valid request_type")

        prepared = request.prepare()
        if signed:
            prepared.headers["Authorization"] = f"bearer {self.access_token}"

        response = self._session.send(prepared, timeout=5)

        data = response.json()

        if "error" in data.keys():
            raise ConnectionError(data["error"])

        return data

    def _connect(self, grand_type: str = "client_credentials") -> None:
        data = self._send_request(
            end_point="/public/auth",
            request_type="GET",
            params={
                "grant_type": grand_type,
                "client_id": self.api_key,
                "client_secret": self.api_secret,
            },
        )["result"]
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        self.end_connection_date = int(time.time()) + data["expires_in"]
        self.connected = True

    def _logout(self) -> None:
        self._send_request(
            end_point="/private/logout", request_type="GET", signed=True
        )["result"]

    def get_server_time(self) -> int:
        ts = self._send_request(
            end_point="/public/ping",
            request_type="GET",
            signed=False,
        )["usOut"]
        return int(ts)

    def get_pairs_info(self, quote_asset: str) -> dict:
        pairs_info: Dict[str, Any] = {}

        data = self._send_request(
            end_point="/public/get_instruments",
            params={"currency": "PERPETUAL"},
            request_type="GET",
        )["result"]

        for info in data:
            if info["is_active"] and info["base_currency"] == quote_asset:
                pair_name = info["instrument_name"]
                pairs_info[pair_name] = {}

                pairs_info[pair_name]["quote_asset"] = info["base_currency"]

                pairs_info[pair_name]["maxLimitQuantity"] = np.Inf
                pairs_info[pair_name]["maxMarketQuantity"] = np.Inf
                pairs_info[pair_name]["minQuantity"] = float(info["min_qty"])

                pairs_info[pair_name]["tick_size"] = float(info["tick_size"])
                pairs_info[pair_name]["step_size"] = float(info["min_trade_amount"])

                pairs_info[pair_name]["creation_timestamp"] = int(
                    info["creation_timestamp"]
                )

        return pairs_info

    @staticmethod
    def _convert_interval(std_interval: str) -> str:
        if "m" in std_interval:
            return std_interval[:-1]

        elif "h" in std_interval:
            mul = int(std_interval[:-1])
            return str(60 * mul)
        else:
            return std_interval[-1].upper()

    def _get_candles(
        self, pair: str, interval: str, start_time: int, end_time: int
    ) -> list:
        _interval = self._convert_interval(std_interval=interval)

        data = self._send_request(
            end_point="/public/get_tradingview_chart_data",
            request_type="GET",
            params={
                "instrument_name": pair,
                "resolution": _interval,
                "start_timestamp": start_time // 1000,
                "end_timestamp": end_time // 1000,
            },
        )

        return data["result"]

    def _get_earliest_timestamp(self, pair: str, interval: str) -> int:
        return int(int(datetime(2018, 1, 1).timestamp() * 1000))

    @staticmethod
    def _format_data(all_data: list) -> pd.DataFrame:
        interval_ms = 1000 * (all_data[1]["tick"] - all_data[0]["tick"])
        df = pd.DataFrame(all_data)[DATA_FORMATING["btcex"]["columns"]]

        for var in DATA_FORMATING["btcex"]["num_var"]:
            df[var] = pd.to_numeric(df[var], downcast="float")

        df = df.rename(columns={"tick": "open_time"})

        df["open_time"] = 1000 * df["open_time"]
        df["close_time"] = df["open_time"] + interval_ms - 1

        return df.dropna()

    def get_historical_data(
        self, pair: str, interval: str, start_ts: int, end_ts: int
    ) -> pd.DataFrame:
        # init our list
        klines = []

        # convert interval to useful value in ms
        timeframe = interval_to_milliseconds(interval)

        # establish first available start timestamp
        if start_ts is not None:
            first_valid_ts = self._get_earliest_timestamp(pair=pair, interval=interval)
            start_ts = max(start_ts, first_valid_ts)

        if end_ts and start_ts and end_ts <= start_ts:
            raise ValueError("end_ts must be greater than start_ts")

        while True:
            # fetch the klines from start_ts up to max 500 entries or the end_ts if set
            temp_data = self._get_candles(
                pair=pair,
                interval=interval,
                start_time=start_ts,
                end_time=start_ts + self.limit * timeframe,
            )

            # append this loops data to our output data
            if temp_data:
                klines += temp_data

            # handle the case where exactly the limit amount of data was returned last loop
            # check if we received less than the required limit and exit the loop
            if not len(temp_data) or len(temp_data) < self.limit:
                # exit the while loop
                break

            # increment next call by our timeframe
            start_ts = 1000 * temp_data[-1]["tick"] + timeframe

            # exit loop if we reached end_ts before reaching <limit> klines
            if end_ts and start_ts >= end_ts:
                break

        df = self._format_data(all_data=klines)

        return df[df["open_time"] <= end_ts]

    def get_extra_market_data(self, pair: str, interval: str) -> pd.DataFrame:
        pass
