import traceback
import json

import pandas as pd
from quantplay.broker.generics.broker import Broker
from quantplay.utils.constant import Constants, timeit
from quantplay.broker.xts_utils.Connect import XTSConnect
from quantplay.utils.pickle_utils import PickleUtils


class XTS(Broker):
    source = "WebAPI"

    @timeit(MetricName="XTS:__init__")
    def __init__(
        self,
        api_secret,
        api_key,
        root_interactive,
        root_market,
    ):
        super(XTS, self).__init__()

        try:
            self.wrapper = XTSConnect(
                apiKey=api_key,
                secretKey=api_secret,
                source=self.source,
                root_interactive=root_interactive,
                root_market=root_market,
            )
            self.login()

        except Exception as e:
            print(traceback.print_exc())
            raise e

        self.initialize_symbol_data()

    def initialize_symbol_data(self):
        try:
            self.symbol_data = PickleUtils.load_data("xts_instruments")
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception as e:
            instruments = pd.read_csv("https://quantplay-public-data.s3.ap-south-1.amazonaws.com/instruments.csv")
            instruments = instruments.to_dict('records')
            self.symbol_data = {}

            for instrument in instruments:
                exchange = instrument['exchange']
                tradingsymbol = instrument['tradingsymbol']
                self.symbol_data["{}:{}".format(exchange, tradingsymbol)] = instrument

            PickleUtils.save_data(self.symbol_data, "xts_instruments")
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from server")

    def login(self):
        response_interact = self.wrapper.interactive_login()
        self.wrapper.marketdata_login()

        self.ClientID = response_interact["result"]["clientCodes"][0]

    def account_summary(self):
        # TODO: Edit For Dealers

        api_response = self.wrapper.get_balance(self.ClientID)

        if not api_response:
            raise Exception(
                "[XTS_ERROR]: Balance API available for retail API users only, dealers can watch the same on dealer terminal"
            )

        api_response = api_response["result"]["BalanceList"][0]["limitObject"]

        response = {
            # TODO: Get PNL
            "pnl": 0,
            "margin_used": api_response["RMSSubLimits"]["marginUtilized"],
            "margin_available": api_response["RMSSubLimits"]["netMarginAvailable"],
        }

        return response

    def profile(self):
        api_response = self.wrapper.get_profile(self.ClientID)["result"]

        response = {
            "user_id": api_response["ClientId"],
            "full_name": api_response["ClientName"],
            "segments": api_response["ClientExchangeDetailsList"],
        }

        return response

    def orders(self):
        # TODO: Transform into Quantplay
        api_response = self.wrapper.get_order_book(self.ClientID)["result"]

        return api_response

    def positions(self):
        # TODO: Transform into Quantplay
        api_response = self.wrapper.get_position_daywise(self.ClientID)["result"]

        return api_response

    def get_exchange_code(self, exchange):
        exchange_code_map = {
            "NSE": 1,
            "NFO": 2,
            "NSECD": 3,
            "BSECM": 11,
            "BSEFO": 12,
        }

        if exchange not in exchange_code_map:
            raise KeyError(
                "INVALID_EXCHANGE: Exchange not in ['NSE', 'NFO', 'NSECD', 'BSECM', 'BSEFO']"
            )

        return exchange_code_map[exchange]

    def get_exchange_name(self, exchange):
        exchange_code_map = {
            "NSE": "NSECM",
            "NFO": "NSEFO",
            "NSECD": "NSECD",
            "BSECM": "BSECM",
            "BSEFO": "BSEFO",
        }

        if exchange not in exchange_code_map:
            raise KeyError(
                "INVALID_EXCHANGE: Exchange not in ['NSE', 'NFO', 'NSECD', 'BSECM', 'BSEFO']"
            )

        return exchange_code_map[exchange]

    def get_ltp(self, exchange=None, tradingsymbol=None):
        exchange_code = self.get_exchange_code(exchange)
        exchange_token = self.symbol_data[f"{exchange}:{tradingsymbol}"]['exchange_token']

        api_response = self.wrapper.get_quote(
            Instruments=[
                {"exchangeSegment": exchange_code, "exchangeInstrumentID": exchange_token}
            ],
            xtsMessageCode=1512,
            publishFormat="JSON",
        )["result"]

        ltp_json = api_response["listQuotes"][0]

        ltp = json.loads(ltp_json)["LastTradedPrice"]

        return ltp

    def place_order(
        self,
        tradingsymbol=None,
        exchange=None,
        quantity=None,
        order_type=None,
        transaction_type=None,
        tag=None,
        product=None,
        price=None,
        trigger_price=0,
    ):
        exchange_code = self.get_exchange_code(exchange)
        exchange_name = self.get_exchange_name(exchange)

        exchange_token = self.symbol_data[f"{exchange}:{tradingsymbol}"]['exchange_token']

        api_response = self.wrapper.place_order(
            exchangeSegment=exchange_name,
            exchangeInstrumentID=exchange_token,
            orderType=order_type,
            disclosedQuantity=0,
            orderQuantity=quantity,
            limitPrice=price,
            timeInForce="DAY",
            stopPrice=trigger_price,
            orderSide=transaction_type,
            productType=product,
            orderUniqueIdentifier=tag,
            clientID=self.ClientID,
        )["result"]

        return api_response["AppOrderID"]

    def cancel_order(self, unique_order_id):
        orders = self.orders()

        tag = list(filter(lambda x: x["AppOrderID"] == int(unique_order_id), orders))[
            0
        ]["OrderUniqueIdentifier"]

        api_response = self.wrapper.cancel_order(
            appOrderID=unique_order_id,
            clientID=self.ClientID,
            orderUniqueIdentifier=tag,
        )

        if api_response["type"] == "error":
            raise Exception("[XTS_ERROR]: " + api_response["description"])

        return api_response["result"]["AppOrderID"]

    def modify_order(
        self,
        order_id,
        price=None,
        trigger_price=None,
        order_type=None,
        transaction_type=None,
        tag=None,
        product=None,
    ):
        orders = self.orders()
        order_data = list(filter(lambda x: x["AppOrderID"] == int(order_id), orders))[0]

        price = price or order_data["OrderPrice"]
        trigger_price = trigger_price or order_data["OrderStopPrice"]
        order_type = order_type or order_data["OrderType"]
        transaction_type = transaction_type or order_data["OrderSide"]
        tag = tag or order_data["OrderUniqueIdentifier"]
        product = product or order_data["ProductType"]

        quantity = order_data["OrderQuantity"]
        time_in_force = "DAY"
        disclosed_quantity = 0

        api_response = self.wrapper.modify_order(
            appOrderID=order_id,
            modifiedTimeInForce=time_in_force,
            modifiedDisclosedQuantity=disclosed_quantity,
            modifiedLimitPrice=price,
            modifiedOrderQuantity=quantity,
            modifiedOrderType=order_type,
            modifiedProductType=product,
            modifiedStopPrice=trigger_price,
            orderUniqueIdentifier=tag,
            clientID=self.ClientID,
        )

        if api_response["type"] == "error":
            raise Exception("[XTS_ERROR]: " + api_response["description"])

        return api_response["result"]["AppOrderID"]

    def modify_price(self, order_id, price, trigger_price=None, order_type=None):
        return self.modify_order(
            order_id=order_id,
            price=price,
            trigger_price=trigger_price,
            order_type=order_type,
        )
