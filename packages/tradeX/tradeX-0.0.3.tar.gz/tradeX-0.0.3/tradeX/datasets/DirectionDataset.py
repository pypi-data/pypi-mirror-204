import numpy as np
import talib

from tradeX.datasets.BinanceDataset import BinanceDataset
from tradeX.datasets.consts import SELECTED_FEATURE_IDX
from scipy.signal import argrelextrema


class DirectionDataset(BinanceDataset):
    EVENT_UP = 1
    EVENT_DOWN = 2
    EVENT_STABLE = 0
    R_MEAN = 11.1565
    R_STD = 9.060607471356432

    def __init__(self, look_ahead, file, look_back, norm=True, limit=-1, feature_engineer=None):
        """
        :param look_ahead:
        :param file:
        :param look_back:
        :param gap: to determine if a candle is up or down. If 0 < abs(openPrice-closePrice) < gap --> STABLE
        :param norm:
        :param limit:
        """
        super(DirectionDataset, self).__init__(file, look_back=look_back, look_ahead=look_ahead, norm=norm,
                                               limit=limit)
        self.feature_engineer = feature_engineer

    def calculate_r(self, lb, all):
        return self.look_ahead
        # ma = talib.EMA(all[:, 0:4].mean(axis=1), timeperiod=4)
        # ma = talib.EMA(ma, timeperiod=2)
        # ma = talib.EMA(ma, timeperiod=2)
        # ma = talib.EMA(ma, timeperiod=2)
        # ma = talib.EMA(ma, timeperiod=2)
        # ma = talib.EMA(ma, timeperiod=2)
        # ma = talib.EMA(ma, timeperiod=2)
        #
        # kline_period = 12
        # local_maximums = argrelextrema(ma, np.greater, order=kline_period)[0]
        # local_minimums = argrelextrema(ma, np.less, order=kline_period)[0]
        #
        # after_lb_local_max = np.nonzero(local_maximums >= lb)[0]
        # after_lb_local_min = np.nonzero(local_minimums >= lb)[0]
        #
        # if len(after_lb_local_min) <= 0 and len(after_lb_local_max) <= 0:
        #     return int(DirectionDataset.R_MEAN)
        # if len(after_lb_local_max) <= 0:
        #     next_min = after_lb_local_min[0]
        #     r = local_minimums[next_min] - lb + 1
        #     return r
        # else:
        #     next_max = after_lb_local_max[0]
        #
        # if len(after_lb_local_min) <= 0:
        #     next_max = after_lb_local_max[0]
        #     r = local_maximums[next_max] - lb + 1
        #     return r
        # else:
        #     next_min = after_lb_local_min[0]
        #
        # if local_maximums[next_max] < local_minimums[next_min]:
        #     return local_maximums[next_max] - lb + 1
        # else:
        #     return local_minimums[next_min] - lb + 1

    def calculate_r_and_theta(self, inp, gt):
        all = np.vstack((inp, gt)).astype(float)
        ma = talib.EMA(all[:, :4].mean(axis=1), timeperiod=2)
        ma = talib.EMA(ma, timeperiod=2)
        ma = talib.EMA(ma, timeperiod=2)
        ma = talib.EMA(ma, timeperiod=2)
        ma = talib.EMA(ma, timeperiod=2)

        lb = len(inp)
        r = self.calculate_r(lb, all)

        theta = self.calculate_theta(ma[-self.look_ahead+2:])

        # current_price = all[:, 3][lb - 1]
        # next_price = ma[lb - 1 + r]
        # theta = np.arctan2(next_price - current_price, 1)
        return theta

    def calculate_theta(self, price):
        x = np.linspace(0, 1, len(price))
        y = price

        # Perform linear regression
        X = np.vstack([x, np.ones(len(price))]).T
        theta = np.linalg.pinv(X) @ y

        # Calculate the angle between the line and the x-axis
        angle = np.arctan(theta[0])
        return angle

    def __getitem__(self, item):
        idx = item + self.look_back
        inp = self.data[item:idx]
        gt = self.data[idx:idx + self.look_ahead]

        # take  9 features, except close & open time
        feature_idx = SELECTED_FEATURE_IDX

        inp = np.array(inp, dtype=np.float32)
        inp = inp[:, feature_idx]

        # take  9 features, except close & open time

        gt = np.array(gt, dtype=np.float32)
        gt = gt[:, feature_idx]

        p_mean = inp[:, 0:4].mean()
        p_std = inp[:, 0:4].std()

        mean = inp.mean(axis=0)
        std = inp.std(axis=0)
        mean[0:4] = p_mean
        std[0:4] = p_std

        inp = (inp - mean) / std
        gt = (gt - mean) / std

        theta = self.calculate_r_and_theta(inp, gt)
        return {
            "input": inp,  # L x 9,
            "theta": theta,
            "mean": mean,
            "std": std,
            "gt": gt
        }

    def __len__(self):
        return len(self.data) - self.look_back - self.look_ahead + 1
