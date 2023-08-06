from binance.enums import SIDE_BUY, SIDE_SELL
from torch.utils.tensorboard import SummaryWriter

from tradeX.bots.binance_bot import BinanceBot
from tradeX.models.EModel import EModel


class LogOnlyBot(BinanceBot):
    """
       This bot is to measure model performance on live market
       """

    def __init__(self, model: EModel, logger: SummaryWriter, *args, **kargs):
        super(LogOnlyBot, self).__init__(*args, **kargs)
        self.model = model
        self.logger = logger
        self.iter = 0
        self.num_trade = 0
        self.__last_position = {"q": 0, "s": 0, "tp": 0}  # q = quantity , s = side, tp = take profit value
        self.num_win = 0
        self.num_lose = 0
        self.last_pred = {"High": 0, "Low": 0, "Close": 0}
        self.acc = {"High": [0, 0], "Low": [0, 0], "Close": [0, 0]}
        self.mse = {"High": 0, "Low": 0, "Close": 0}

    def summary_past(self, past_data):
        o, h, l, c = float(past_data[-1][1]), float(past_data[-1][2]), float(past_data[-1][3]), float(past_data[-1][4])

        # log GT
        self.logger.add_scalar("High/GT", h, self.iter)
        self.logger.add_scalar("Low/GT", l, self.iter)
        self.logger.add_scalar("Close/GT", c, self.iter)

        # calculate profit and log USD
        profit = 0
        if self.__last_position["s"] == SIDE_BUY:
            profit = self.estimate_profit_market_then_limit(SIDE_BUY, o, self.usd, 0.95, self.__last_position["tp"], 1)
            if h > self.__last_position["tp"]:
                self.num_win += 1
            else:
                self.num_lose += 1
            self.usd += profit
        if self.__last_position["s"] == SIDE_SELL:
            profit = self.estimate_profit_market_then_limit(SIDE_SELL, o, self.usd, 0.95, self.__last_position["tp"], 1)
            if l < self.__last_position["tp"]:
                self.num_win += 1
            else:
                self.num_lose += 1
        self.usd += profit
        self.logger.add_scalar("USD", self.usd, self.iter)

        # reset position
        self.__last_position = {"s": 0, "enter": 0, "q": 0,
                                "tp": 0}  # always close position as new interval if TP or SL was not reached

        self.logger.add_scalar("Trade/num_win", self.num_win, self.iter)
        self.logger.add_scalar("Trade/num_lose", self.num_lose, self.iter)

        # log model performance
        for idx, k in enumerate(self.last_pred):
            if self.last_pred[k] != 0:
                num_preds = sum(self.acc[k]) + 1

                # mse
                self.mse[k] = (self.mse[k] * (num_preds - 1) + abs(
                    self.last_pred[k] - float(past_data[-1][idx + 2]))) / num_preds

                # binary acc
                is_up_gt = float(past_data[-1][idx + 2]) - float(past_data[-2][idx + 2])
                is_up_pred = self.last_pred[k] - float(past_data[-2][idx + 2])
                if is_up_pred * is_up_gt > 0:
                    self.acc[k][0] += 1  # right
                else:
                    self.acc[k][1] += 1  # wrong

                # log
                self.logger.add_scalar(f"{k}/right", self.acc[k][0], sum(self.acc[k]))
                self.logger.add_scalar(f"{k}/wrong", self.acc[k][1], sum(self.acc[k]))
                self.logger.add_scalar(f"{k}/l1", self.mse[k], sum(self.acc[k]))

    def on_start(self):
        print("Start==============================================")

    def on_new_interval(self, pdata):
        # calculate_acc
        self.summary_past(pdata)

        # predict and place order next round
        h, l, c = float(pdata[-1][2]), float(pdata[-1][3]), float(pdata[-1][4])
        ph, pl, pc = self.model.predict(pdata, ahead=1)
        ph, pl, pc = round(ph), round(pl), round(pc)

        profit_l = self.estimate_profit_market_then_limit(SIDE_BUY, c, self.usd, 0.95, limit_price=ph,
                                                          leverage=10)
        profit_s = self.estimate_profit_market_then_limit(SIDE_SELL, c, self.usd, 0.95, limit_price=pl,
                                                          leverage=10)

        if profit_l > profit_s > 0 and ph > h and pl > l:
            self.num_trade += 1
            self.__last_position = {"s": SIDE_BUY, "enter": c, "tp": ph}

        elif profit_s > profit_l > 0 and pl < l and ph < h:
            self.num_trade += 1
            self.__last_position = {"s": SIDE_SELL, "enter": c, "tp": pl}

        self.logger.add_scalar("Trade/profit_if_place", max(profit_s, profit_s), self.iter)
        self.logger.add_scalar("Trade/Num_all", self.num_trade, self.iter)

        # below is logging for model optimization purpose
        self.last_pred["High"] = ph
        self.last_pred["Low"] = pl
        self.last_pred["Close"] = pc

        self.logger.add_scalar("High/Pred", ph, self.iter + 1)
        self.logger.add_scalar("Low/Pred", pl, self.iter + 1)
        self.logger.add_scalar("Close/Pred", pc, self.iter + 1)

        self.iter += 1
