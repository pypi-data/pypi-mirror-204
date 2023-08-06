# from datetime import datetime, timedelta

# from novalabs.utils.backtest import BackTest


# def asserts_get_historical_data(test: dict) -> None:
#     back = BackTest(
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

#     for pair in test["list_pairs"]:
#         back.get_historical_data(pair=pair)

#     print(f"Test get_historical_data for {test['exchange'].upper()} SUCCESSFUL")


# def test_asserts_get_historical_data() -> None:
#     all_test = [
#         {
#             "exchange": "binance",
#             "list_pairs": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
#         }
#     ]

#     for test in all_test:
#         asserts_get_historical_data(test)


# test_asserts_get_historical_data()
