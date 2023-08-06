import numpy as np
from binance.enums import SIDE_BUY, SIDE_SELL
from torch.utils.tensorboard import SummaryWriter

from tradeX.bots.binance_bot import BinanceBot
from tradeX.models.EModel import EModel


class SimpleBot(BinanceBot):
    """
    Simple Futures trading bot. In every new interval:
    1. Cancel all orders
    2. Close all positions
    3. Make prediction (high, low, close) with AI model
    4. Long/short and set take profit at a threshold
    """

    class Intent:
        def __init__(self, low, high):
            self.low = low
            self.high = high

    def __init__(self, model: EModel, logger: SummaryWriter, *args, **kargs, ):
        super(SimpleBot, self).__init__(*args, **kargs)
        self.model = model
        self.logger = logger
        self.iter = 0
        self.intent: SimpleBot.Intent = None

    def on_start(self):
        self.logger.add_scalar("USD", self.balance_usd(fetch_from_cache=False), self.iter)

    def on_new_interval(self, pdata):
        # cancel all orders
        self.cancel_all_orders()
        self.cancel_all_positions()
        self.intent = None

        # log GT
        o, h, l, c = float(pdata[-1][1]), float(pdata[-1][2]), float(pdata[-1][3]), float(pdata[-1][4])
        self.logger.add_scalars("GT", {"High": h, "Low": l, "Close": c}, self.iter)

        # log USD
        self.logger.add_scalar("USD", self.balance_usd(fetch_from_cache=False), self.iter)
        if self.balance_usd(fetch_from_cache=True) < 10:
            exit(0)
        # predict and place order next round
        ph, pl, pc = self.model.predict(pdata)
        ph, pl, pc = round(ph), round(pl), round(pc)

        profit = self.estimate_profit_limit_then_limit(SIDE_BUY, pl, self.balance_usd(fetch_from_cache=True), 0.5,
                                                       exit_price=ph,
                                                       leverage=10)
        if profit > 0:
            self.intent = SimpleBot.Intent(low=pl, high=ph)
            print("Intent", pl, ph)

        self.logger.add_scalars("Pred", {"High": ph, "Low": pl, "Close": pc}, self.iter + 1)
        self.iter += 1

    def on_tik(self, realtime_data):
        data = np.array(realtime_data).astype(float).tolist()
        _, o, h, l, c, *_ = data  # c = current price
        if self.intent is not None:
            if self.position is None:  # this mean the intent is not started yet
                if c - self.intent.low < -1:
                    self.long_market(percent_asset=0.5, leverage=10)
                elif self.intent.high - c < -1:
                    self.short_market(percent_asset=0.5, leverage=10)
            else:  # this means there is a position, time to take profit
                if self.position.s == SIDE_BUY and self.intent.high - c < 0:
                    self.stop_market(SIDE_SELL, self.position.q)
                    self.intent = None
                elif self.position.s == SIDE_SELL and c - self.intent.low < 0:
                    self.stop_market(SIDE_BUY, self.position.q)
                    self.intent = None
