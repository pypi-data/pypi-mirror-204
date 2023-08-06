import ast
import asyncio
import time

import numpy as np
from loguru import logger
from websocket import WebSocketApp

from tradeX.bots.consts import INTERVAL_2_SECONDS
from tradeX.utils.data_getter import get_data_all_the_time


class BinanceDataBot:
    def __init__(self, symbol, interval, look_back=100, data_delay_allowed=5000, stop_on_err=True):
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

    def on_tik(self, realtime_data):
        """Real time data update"""
        return

    def on_start(self):
        logger.info("BOT Start")

    def on_new_interval(self, past_data):
        raise "Unimplemented yet"

    async def reset_data(self):
        dfrom = int(time.time() * 1000) - INTERVAL_2_SECONDS[self.interval] * (self.look_back * 2) * 1000
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
