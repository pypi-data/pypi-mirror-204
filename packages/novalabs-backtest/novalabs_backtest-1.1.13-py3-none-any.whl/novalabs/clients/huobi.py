import base64
import hashlib
import hmac
import time
import urllib.parse as parse
from datetime import datetime
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
from requests import Request, Session

from novalabs.interfaces.client_interface import ClientInterface
from novalabs.utils.helpers import interval_to_milliseconds


class Huobi(ClientInterface):
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

        self.based_endpoint = "https://api.hbdm.com"
        self._session = Session()

    def _send_request(
        self,
        end_point: str,
        request_type: str,
        params: Optional[Dict[str, Any]] = {},
        signed: bool = False,
    ) -> dict:
        uri = f"{self.based_endpoint}{end_point}"

        if signed:
            sign_params = params if params else {}

            sign_params.update(
                {
                    "AccessKeyId": self.api_key,
                    "SignatureMethod": "HmacSHA256",
                    "SignatureVersion": "2",
                    "Timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )
            sorted_params = sorted(
                sign_params.items(), key=lambda d: d[0], reverse=False
            )
            encode_params = parse.urlencode(sorted_params)
            host_url = self.based_endpoint.replace("https://", "")
            payload = [request_type, host_url, end_point, encode_params]
            payload_str = "\n".join(payload)
            hash_ = hmac.new(
                self.api_secret.encode(encoding="utf8"),
                payload_str.encode(encoding="UTF8"),
                digestmod=hashlib.sha256,
            )
            signature = base64.b64encode(hash_.digest())
            sign_params["Signature"] = signature.decode()

            request = Request(request_type, uri, params=sign_params, json=params)
        else:
            request = Request(request_type, uri, params=params)

        prepared = request.prepare()
        prepared.headers["User-Agent"] = "Novalabs.ai"
        if request_type == "GET":
            prepared.headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            prepared.headers["Accept"] = "application/json"
            prepared.headers["Content-Type"] = "application/json"
        response = self._session.send(prepared)
        return response.json()

    def get_server_time(self) -> int:
        ts = self._send_request(end_point="/api/v1/timestamp", request_type="GET")["ts"]
        return int(ts)

    def get_pairs_info(self, quote_asset: str) -> dict:
        contracts = self._send_request(
            end_point="/linear-swap-api/v1/swap_contract_info",
            request_type="GET",
            params={},
        )["data"]

        pairs_info: Dict[str, Any] = {}

        for contract in contracts:
            tradable = contract["contract_status"] == 1

            if tradable and quote_asset == contract["trade_partition"]:
                pairs_info[contract["contract_code"]] = {}

                pairs_info[contract["contract_code"]]["quote_asset"] = contract[
                    "trade_partition"
                ]

                pairs_info[contract["contract_code"]]["maxQuantity"] = np.Inf
                pairs_info[contract["contract_code"]]["minQuantity"] = np.Inf

                pairs_info[contract["contract_code"]]["tick_size"] = contract[
                    "price_tick"
                ]
                if pairs_info[contract["contract_code"]]["tick_size"] < 1:
                    step_size = str(contract["price_tick"])[::-1].find(".")
                    pairs_info[contract["contract_code"]]["pricePrecision"] = int(
                        step_size
                    )
                else:
                    pairs_info[contract["contract_code"]]["pricePrecision"] = 1

                pairs_info[contract["contract_code"]]["step_size"] = contract[
                    "contract_size"
                ]

                if pairs_info[contract["contract_code"]]["step_size"] < 1:
                    step_size = str(contract["contract_size"])[::-1].find(".")
                    pairs_info[contract["contract_code"]]["quantityPrecision"] = int(
                        step_size
                    )
                else:
                    pairs_info[contract["contract_code"]]["quantityPrecision"] = 1

        return pairs_info

    @staticmethod
    def _convert_interval(std_interval: str) -> str:
        mul = int(std_interval[:-1])
        if "m" in std_interval:
            return f"{mul}min"
        elif "h" in std_interval and int(mul) == 1:
            return "60min"
        elif "h" in std_interval:
            return f"{mul}hour"
        elif "d" in std_interval:
            return f"{mul}day"
        else:
            return "Wrong Input"

    def _get_candles(
        self, pair: str, interval: str, start_time: int, end_time: int
    ) -> list:
        data = self._send_request(
            end_point="/linear-swap-ex/market/history/kline",
            request_type="GET",
            params={
                "contract_code": pair,
                "period": self._convert_interval(std_interval=interval),
                "size": self.limit,
                "from": start_time // 1000,
                "to": end_time // 1000,
            },
        )
        return data["data"]

    def _get_earliest_timestamp(self, pair: str, interval: str) -> int:
        contracts = self._send_request(
            end_point="/linear-swap-api/v1/swap_contract_info",
            request_type="GET",
            params={"contract_code": pair},
        )["data"]

        dt = datetime.strptime(contracts[0]["create_date"], "%Y%m%d")
        return int(dt.timestamp() * 1000)

    @staticmethod
    def _format_data(all_data: list) -> pd.DataFrame:
        df = pd.DataFrame.from_records(all_data)

        df = df.rename(
            columns={
                "id": "open_time",
                "amount": "volume",
                "trade_turnover": "quote_asset_volume",
                "count": "nb_of_trades",
            }
        )

        df = df.drop(columns=["vol"])
        df["open_time"] = 1000 * df["open_time"]
        interval_ms = 1000 * (all_data[1]["id"] - all_data[0]["id"])
        df["close_time"] = df["open_time"] + interval_ms - 1
        return df

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

        start_time = max(start_ts, first_valid_ts) + timeframe

        idx = 0

        while True:
            end_t = int(start_time + timeframe * self.limit)
            end_time = min(end_t, end_ts)

            print(
                f"start_time : {start_time} and end_time : {end_time} -- {end_time - start_time}"
            )

            # fetch the klines from start_ts up to max 500 entries or the end_ts if set
            temp_data = self._get_candles(
                pair=pair, interval=interval, start_time=start_time, end_time=end_time
            )

            # append this loops data to our output data
            if temp_data:
                klines += temp_data

            # handle the case where exactly the limit amount of data was returned last loop
            # check if we received less than the required limit and exit the loop

            print(f"{len(temp_data)} -- {self.limit}")

            if len(temp_data) < self.limit:
                print("inside 1")
                break

            # increment next call by our timeframe
            start_time = 1000 * temp_data[-1]["id"] + timeframe
            # exit loop if we reached end_ts before reaching <limit> klines
            if end_ts and start_time >= end_ts:
                print("inside 1")
                break

            idx += 1
            if idx % 3 == 0:
                time.sleep(1)

        data = self._format_data(all_data=klines)

        return data[(data["open_time"] >= start_ts) & (data["open_time"] <= end_ts)]

    def get_extra_market_data(self, pair: str, interval: str) -> pd.DataFrame:
        pass
