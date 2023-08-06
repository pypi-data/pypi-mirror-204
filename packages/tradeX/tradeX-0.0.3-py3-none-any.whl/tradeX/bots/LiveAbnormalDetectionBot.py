from binance.enums import SIDE_BUY, SIDE_SELL
from torch.utils.tensorboard import SummaryWriter

from tradeX.bots.binance_bot import BinanceBot
from tradeX.models.EModel import EModelClassifier

import numpy as np


class LiveAbnormalDetectionBot(BinanceBot):
    """
           This bot is to measure model performance on live market
           """

    def __init__(self, model: EModelClassifier, logger: SummaryWriter, *args, **kargs):
        super(LiveAbnormalDetectionBot, self).__init__(*args, **kargs)
        self.model = model
        self.logger = logger
        self.leverage = 10
        self.iter = 0
        self.lose = 0
        self.win = 0

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
        # self.logger.add_scalar("Performance/Win", self.win, self.iter)
        # self.logger.add_scalar("Performance/Lose", self.lose, self.iter)
        self.logger.add_scalar("USD", self.balance_usd())

        bump, dump = self.model.predict(pdata)
        print(bump, dump)
        if bump > dump > 0.11:
            if self.position is not None:
                if self.position.s != SIDE_BUY:
                    self.cancel_all_positions()
                    self.long_market(0.9, self.leverage)
            else:
                self.long_market(0.9, self.leverage)

        elif dump > bump > 0.11:
            if self.position is not None:
                if self.position.s != SIDE_SELL:
                    self.cancel_all_positions()
                    self.short_market(0.9, self.leverage)
            else:
                self.short_market(0.9, self.leverage)
