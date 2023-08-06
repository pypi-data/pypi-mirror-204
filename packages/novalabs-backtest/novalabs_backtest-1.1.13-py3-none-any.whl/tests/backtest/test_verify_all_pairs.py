# from datetime import datetime, timedelta

# from novalabs.utils.backtest import BackTest


# def asserts_verify_all_pairs(test: dict) -> None:
#     """
#     When Instantiating Backtest -> self._verify_all_pairs() is called !
#     """
#     BackTest(
#         exchange=test["exchange"],
#         strategy_name="",
#         candle="1h",
#         list_pairs=test["list_pairs"],
#         start=datetime(2020, 1, 1),
#         end=datetime(2023, 1, 1),
#         start_bk=1000,
#         leverage=5,
#         max_pos=2,
#         max_holding=timedelta(hours=12),
#         quote_asset="USDT",
#         geometric_sizes=False,
#         plot_all_pairs_charts=False,
#         plot_exposure=False,
#         api_key="",
#         api_secret="",
#         passphrase="",
#         backtest_id="",
#     )

#     print(f"Test _verify_all_pairs for {test['exchange'].upper()} SUCCESSFUL")


# def test_verify_all_pairs() -> None:
#     all_test = [
#         {
#             "exchange": "binance",
#             "list_pairs": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
#             "result": "pass",
#         }
#     ]

#     for test in all_test:
#         asserts_verify_all_pairs(test)


# test_verify_all_pairs()
