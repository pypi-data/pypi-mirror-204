import ripio
import datetime as dt
from ripio.trade.client import Client

ripio.api_key = "U2FsdGVkX1+XtVrDRsxsAkMgY9zUpuLHDDVFegsTfAk8gzfLG99IYram7yVkcfIU"  # noqa:E501
new_trade = Client()
# orders = new_trade.get_orders(pair="ETH_BRL")
# # print(order)
# print(new_trade.get_orders(pair="ETH_BRL"))
# # order_params = {
# #     "pair": "ETH_BRL",
# #     "side": "sell",
# #     "type": "market",
# #     "value": 10,
# # }
# # order = new_trade.create_order(**order_params)

# new_trade.get_tickers()
# print(new_trade.get_open_orders(pair="ETH_BRL", side="buy"))
# print(new_trade.get_order_by_id(id="02601618-18C2-4227-8437-EE2CBAC5D40C"))
# print(new_trade.cancel_all_orders())
print("_______________Tickers________________________")
print(new_trade.get_tickers())
print("_______________TickerPairs________________________")
print(new_trade.get_ticker_by_pair(pair="BTC_BRL"))
print("_______________Orderbook 3________________________")
print(new_trade.get_orderbook_level_3(pair="BTC_BRL"))
print("_______________Orderbook 2________________________")
print(new_trade.get_orderbook_level_2(pair="BTC_BRL"))
print("_______________Trades________________________")
print(new_trade.get_trades(pair="BTC_BRL"))
print("_______________Currencies________________________")
print(new_trade.get_currencies())
print("_______________Pairs________________________")
print(new_trade.get_pairs())
print("_______________Server Time________________________")
print(new_trade.get_server_time())
print("***************BOOK SECTION***********************")
print(new_trade.get_book_summary("BTC_BRL"))
print("_______________Estimate price___________________")
print(new_trade.get_book_estimate_price(pair="BTC_BRL", amount="10", side="sell"))
print("_______________Book OrderBook Level 3___________")
print(new_trade.get_book_orderbook_level_3(pair="BTC_BRL"))
print("_______________Book OrderBook Level 2___________")
print(new_trade.get_book_orderbook_level_2(pair="BTC_BRL"))
print("***************USER SECTION***********************")
print(new_trade.get_user_balances())
print("_______________User get balance for date__________")
print(new_trade.get_user_balance_on_date(dt.date(2023,1,26)))
print("_______________User get fees and limits__________")
print(new_trade.get_user_fee_and_limits())
print("_______________User statements___________________")
print(new_trade.get_user_statement())
print("_______________User get statement by currency code______")
print(new_trade.get_user_statement_by_currency("BTC"))
print("_______________User get trades___________________")
print(new_trade.get_user_trades())
print("***************DEPOSITS SECTION***********************")
print(new_trade.get_deposits("BTC", "confirmed"))
