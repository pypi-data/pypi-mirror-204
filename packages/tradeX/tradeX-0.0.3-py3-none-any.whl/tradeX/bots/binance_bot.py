import ast
import asyncio
import time

import numpy as np
from binance import Client
from binance.enums import SIDE_BUY, SIDE_SELL, FUTURE_ORDER_TYPE_MARKET, FUTURE_ORDER_TYPE_STOP_MARKET, \
    FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET, FUTURE_ORDER_TYPE_TAKE_PROFIT, FUTURE_ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC
from loguru import logger
from websocket import WebSocketApp

from tradeX.bots.consts import INTERVAL_2_SECONDS, Mode_DryRun, Mode_Live, Mode_Testnet
from tradeX.utils.data_getter import _get_data_chunk, get_data_all_the_time


class BinanceBot:
    class Position:
        def __init__(self, q, s, entry=0):
            self.q = q
            self.s = s
            self.entry = entry

    def __init__(self, symbol, interval, look_back=100, data_delay_allowed=5000, stop_on_err=True, usd=0):
        self.symbol = symbol
        self.interval = interval
        self.look_back = look_back
        self.data_delay_allowed = data_delay_allowed
        self.data = []
        self.stop_on_err = stop_on_err
        self.socket = WebSocketApp(
            f"wss://fstream.binance.com/stream?streams={self.symbol}@kline_{self.interval}",
            on_message=self.on_message,
            on_error=self.on_error)
        self.client: Client
        self.position: BinanceBot.Position = None  # list of Positions objects
        self.__run_mode = Mode_DryRun
        self.usd = usd

    @staticmethod
    def ws_data_to_kline_data(ws_data):
        open_t = ws_data['t']
        open = ws_data['o']
        high = ws_data['h']
        low = ws_data['l']
        close = ws_data['c']
        volume = ws_data['v']
        close_t = ws_data['T']
        qv = ws_data['q']
        n = ws_data['n']
        tbbav = ws_data['V']
        tbqav = ws_data['Q']
        ignore = ws_data['B']
        return [open_t, open, high, low, close, volume, close_t, qv, n, tbbav, tbqav, ignore]

    def estimate_profit_limit_then_limit(self, side, entry_price, current_usd, percent_asset, exit_price, leverage):
        """
        roughly estimate if LONG/SHORT limit then STOP/TAKE_PROFIT limit
        """
        usd = current_usd
        q = round(usd * percent_asset * leverage / entry_price, 3)

        fee1 = 0.02 / 100 * q * entry_price
        fee2 = 0.02 / 100 * q * exit_price

        if side == SIDE_SELL:
            return (1 / exit_price - 1 / entry_price) * q * entry_price * exit_price - fee1 - fee2
        else:
            return (1 / entry_price - 1 / exit_price) * q * entry_price * exit_price - fee1 - fee2

    def estimate_profit_market_then_limit(self, side, mark_price, current_usd, percent_asset, limit_price, leverage):
        """
        roughly estimate if LONG/SHORT market then STOP/TAKE_PROFIT limit
        """
        usd = current_usd
        q = round(usd * percent_asset * leverage / mark_price, 3)

        fee1 = 0.04 / 100 * q * mark_price
        fee2 = 0.02 / 100 * q * limit_price

        if side == SIDE_SELL:
            return (1 / limit_price - 1 / mark_price) * q * mark_price * limit_price - fee1 - fee2
        else:
            return (1 / mark_price - 1 / limit_price) * q * mark_price * limit_price - fee1 - fee2

    def warning_if_there_is_open_position(self, order_type: str):
        if self.position is not None:
            logger.warning(f"Not allow to place {order_type} order due to there is an opening position")

    def long_market(self, percent_asset=0.9, leverage=1):
        """
        :param percent_asset: control how much of USD to place this order, 1 means ALL IN
        :param leverage:
        :return:
        """
        assert self.__run_mode != Mode_DryRun
        self.warning_if_there_is_open_position(order_type="long market")
        try:
            self.client.futures_change_leverage(symbol=self.symbol, leverage=leverage)
            usd = self.balance_usd()
            p = self.market_price()
            q = round(usd / p * percent_asset * leverage, 3)
            res = self.client.futures_create_order(
                symbol=self.symbol,
                side=SIDE_BUY,
                type=FUTURE_ORDER_TYPE_MARKET,
                quantity=q
            )
            self.position = BinanceBot.Position(q=q, s=SIDE_BUY)
            return res
        except Exception as e:
            logger.exception(e)

    def long_limit(self, price, percent_asset=0.9, leverage=1):
        """
        :param percent_asset: control how much of USD to place this order, 1 means ALL IN
        :param leverage:
        :return:
        """
        assert self.__run_mode != Mode_DryRun
        self.warning_if_there_is_open_position(order_type="long limit")
        try:
            self.client.futures_change_leverage(symbol=self.symbol, leverage=leverage)
            usd = self.balance_usd()
            p = self.market_price()
            q = round(usd / p * percent_asset, 3)
            res = self.client.futures_create_order(
                symbol=self.symbol,
                side=SIDE_BUY,
                type=FUTURE_ORDER_TYPE_LIMIT,
                quantity=q,
                timeInForce=TIME_IN_FORCE_GTC,
                price=price
            )
            self.position = BinanceBot.Position(q=q, s=SIDE_BUY)
            return res
        except Exception as e:
            logger.exception(e)

    def short_market(self, percent_asset=0.9, leverage=1):
        """
                :param percent_asset: control how much of USD to place this order, 1 means ALL IN
                :param leverage:
                :return:
                """
        assert self.__run_mode != Mode_DryRun
        self.warning_if_there_is_open_position(order_type="short market")
        try:
            self.client.futures_change_leverage(symbol=self.symbol, leverage=leverage)
            usd = self.balance_usd()
            p = self.market_price()
            q = round(usd / p * percent_asset * leverage, 3)
            res = self.client.futures_create_order(
                symbol=self.symbol,
                side=SIDE_SELL,
                type=FUTURE_ORDER_TYPE_MARKET,
                quantity=q
            )
            self.position = BinanceBot.Position(s=SIDE_SELL, q=q)
            return res
        except Exception as e:
            logger.exception(e)

    def short_limit(self, price, percent_asset=0.9, leverage=1):
        """
                :param percent_asset: control how much of USD to place this order, 1 means ALL IN
                :param leverage:
                :return:
                """
        assert self.__run_mode != Mode_DryRun
        self.warning_if_there_is_open_position(order_type="short limit")
        try:
            self.client.futures_change_leverage(symbol=self.symbol, leverage=leverage)
            usd = self.balance_usd()
            p = self.market_price()
            q = round(usd / p * percent_asset, 3)
            res = self.client.futures_create_order(
                symbol=self.symbol,
                side=SIDE_SELL,
                type=FUTURE_ORDER_TYPE_LIMIT,
                quantity=q,
                price=price,
                timeInForce=TIME_IN_FORCE_GTC,
            )
            self.position = BinanceBot.Position(s=SIDE_SELL, q=q)
            return res
        except Exception as e:
            logger.exception(e)

    def stop_market(self, side, q):
        assert self.__run_mode != Mode_DryRun
        try:
            self.client.futures_create_order(symbol=self.symbol, side=side,
                                             type=FUTURE_ORDER_TYPE_MARKET, quantity=q, closePosition=True)
        except Exception as e:
            logger.exception(e)

    def take_profit_market(self, stop_price, side):
        assert self.__run_mode != Mode_DryRun
        try:
            self.client.futures_create_order(symbol=self.symbol, stopPrice=stop_price, side=side,
                                             type=FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET, closePosition=True)
        except Exception as e:
            logger.exception(e)

    def take_profit_limit(self, side, stop_price, price):
        assert self.__run_mode != Mode_DryRun
        try:
            self.client.futures_create_order(symbol=self.symbol, stopPrice=stop_price, price=price, side=side,
                                             type=FUTURE_ORDER_TYPE_TAKE_PROFIT, closePosition=True)
        except Exception as e:
            logger.exception(e)

    def cancel_all_positions(self):
        assert self.__run_mode != Mode_DryRun
        try:
            if self.position is not None and self.position.q > 0:
                t = SIDE_SELL if self.position.s == SIDE_BUY else SIDE_BUY
                self.client.futures_create_order(symbol=self.symbol, type=FUTURE_ORDER_TYPE_MARKET,
                                                 side=t, quantity=self.position.q)
                self.position = None
        except Exception as e:
            logger.exception(e)

    def cancel_all_orders(self):
        assert self.__run_mode != Mode_DryRun
        for i in range(3):
            # make 3 attempts to cancel until OK
            try:
                res = self.client.futures_cancel_all_open_orders(symbol=self.symbol)
                if res["code"] == 200:
                    return
            except Exception as e:
                logger.exception(e)

    def on_tik(self, realtime_data):
        """Real time data update"""
        return

    def on_start(self):
        logger.info("BOT Start")

    def market_price(self):
        return float(self.client.futures_mark_price(symbol=self.symbol)["markPrice"])

    def balance_usd(self, fetch_from_cache=False):
        assert self.__run_mode != Mode_DryRun
        if fetch_from_cache is False:
            accounts = self.client.futures_account_balance()
            for a in accounts:
                if a["asset"] == "USDT":
                    self.usd = float(a["balance"])
                    return self.usd
            return self.usd
        else:
            return self.usd

    def on_new_interval(self, past_data):
        raise "Unimplemented yet"

    async def reset_data(self):
        dfrom = int(time.time() * 1000) - INTERVAL_2_SECONDS[self.interval] * (self.look_back * 2) * 1000
        # self.data = _get_data_chunk(self.symbol, dfrom, self.interval)[-self.look_back - 1:-1]
        self.data = get_data_all_the_time(self.symbol, dfrom, self.interval, save_path=None)[-self.look_back - 1:-1]

    async def reset_data_util_valid(self, sleep_seconds):
        await self.reset_data()
        while self.validate_data() is False:
            await asyncio.sleep(sleep_seconds)
            await self.reset_data()

    async def loop(self):
        await self.reset_data()
        self.on_start()
        await self.reset_data_util_valid(4)
        logger.info("Data prepare OK")
        self.socket.run_forever()

    def validate_data(self):
        if self.data is None:
            return False
        if len(self.data) != self.look_back:
            return False
        old_t = self.data[-1][0]
        if old_t + INTERVAL_2_SECONDS[self.interval] * 1000 * 1.25 < time.time() * 1000:
            return False
        if old_t + INTERVAL_2_SECONDS[self.interval] * 1000 > time.time() * 1000:
            return False
        if np.count_nonzero(
                np.diff([item[0] for item in self.data]) != INTERVAL_2_SECONDS[self.interval] * 1000):
            return False
        return True

    def on_message(self, ws, message):
        data = ast.literal_eval(message.replace("true", "True").replace("false", "False"))["data"]
        logger.debug(data)
        tdata = data["E"]

        t = time.time() * 1000  # seconds
        if t - tdata < self.data_delay_allowed:
            self.on_tik(self.ws_data_to_kline_data(data['k']))

        if data["k"]["x"] == True:
            self.data.append(self.ws_data_to_kline_data(data['k']))
            self.data = self.data[-self.look_back:]
            if self.validate_data() is False:
                logger.warning("Data invalid, need fix")
                self.reset_data_util_valid(4)
                logger.info("Fixing data done")
        else:
            return

        t = time.time() * 1000  # seconds
        if t - tdata < self.data_delay_allowed:
            logger.info("New interval")
            self.on_new_interval(self.data)

    def on_error(self, wsapp, err):
        logger.error(err)
        if self.stop_on_err:
            self.socket.close()

    async def dry_run(self):
        print("Running in dry mode")
        self.__run_mode = Mode_DryRun
        self.client = Client(testnet=False)
        await self.loop()

    async def run_on_testnet(self, api_key, api_secret):
        self.__run_mode = Mode_Testnet
        self.client = Client(api_key, api_secret, testnet=True)
        await self.loop()

    async def run_live(self, api_key, api_secret):
        self.__run_mode = Mode_Live
        self.client = Client(api_key, api_secret, testnet=False)
        await self.loop()
