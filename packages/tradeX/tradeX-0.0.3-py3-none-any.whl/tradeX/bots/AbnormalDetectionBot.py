from binance.enums import SIDE_BUY, SIDE_SELL
from torch.utils.tensorboard import SummaryWriter

from tradeX.bots.binance_bot import BinanceBot
from tradeX.models.EModel import EModelClassifier

import numpy as np


class AbnormalDetectionBot(BinanceBot):
    """
           This bot is to measure model performance on live market
           """

    def __init__(self, model: EModelClassifier, logger: SummaryWriter, *args, **kargs):
        super(AbnormalDetectionBot, self).__init__(*args, **kargs)
        self.model = model
        self.logger = logger
        self.leverage = 10
        self.iter = 0
        self.track = {"position": self.position, "iter": self.iter, "usd_at_entry": self.usd}
        self.lose = 0
        self.win = 0

    def open_track(self, current_price, side):
        q = round(self.usd * self.leverage / current_price, 3)
        fee = q * current_price * 0.04 / 100
        self.track["usd_at_entry"] = self.usd
        self.usd -= fee
        self.track["position"] = BinanceBot.Position(q=q, s=side, entry=current_price)
        self.track["iter"] = self.iter

    def close_track(self, current_price):
        t = self.track
        p = self.track["position"]
        if p is not None:
            q = p.q
            s = p.s
            fee = q * current_price * 0.04 / 100
            profit = q * (current_price - p.entry) * (1 if s == SIDE_BUY else -1)
            before = t["usd_at_entry"]
            self.usd = before - fee + profit
            self.track["position"] = None
            self.track["iter"] = 0
            if self.usd <= before:
                self.lose += 1
            else:
                self.win += 1

    def on_start(self):
        print("Start==============================================")

    def on_tik(self, realtime_data):
        data = np.array(realtime_data).astype(float).tolist()
        _, o, h, l, c, *_ = data  # c = current price
        t = self.track
        p = t["position"]
        estimate_usd = self.usd
        if p is not None:
            estimate_usd += (c - p.entry) * p.q * (1 if p.s == SIDE_BUY else -1)
        self.logger.add_scalar("USD", estimate_usd, self.iter)

    def on_new_interval(self, pdata):
        """
        :param pdata: array of size self.look_back x 12
        :return:
        """
        self.iter += 1
        self.logger.add_scalar("Performance/Win", self.win, self.iter)
        self.logger.add_scalar("Performance/Lose", self.lose, self.iter)

        current_price = float(pdata[-1][4])

        if self.track["position"] is not None and self.track["iter"] >= 15:
            self.close_track(current_price)

        bump, dump = self.model.predict(pdata)
        if bump > dump > 0.1:
            if self.track["position"] is not None:
                if self.track["position"].s != SIDE_BUY:
                    self.close_track(current_price)
                    self.open_track(current_price, side=SIDE_BUY)
            else:
                self.open_track(current_price, side=SIDE_BUY)

        elif dump > bump > 0.1:
            if self.track["position"] is not None:
                if self.track["position"].s != SIDE_SELL:
                    self.close_track(current_price)
                    self.open_track(current_price, side=SIDE_SELL)
            else:
                self.open_track(current_price, side=SIDE_SELL)
