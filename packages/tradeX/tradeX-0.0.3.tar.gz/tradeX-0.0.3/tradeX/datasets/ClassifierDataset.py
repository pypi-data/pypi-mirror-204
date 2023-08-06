import numpy as np

from tradeX.datasets.BinanceDataset import BinanceDataset
from tradeX.datasets.consts import SELECTED_FEATURE_IDX


class ClassifierDataset(BinanceDataset):
    EVENT_UP = 1
    EVENT_DOWN = 2
    EVENT_STABLE = 0

    def __init__(self, look_ahead, file, look_back, gap=100, norm=True, limit=-1, feature_engineer=None):
        """
        :param look_ahead:
        :param file:
        :param look_back:
        :param gap: to determine if a candle is up or down. If 0 < abs(openPrice-closePrice) < gap --> STABLE
        :param norm:
        :param limit:
        """
        super(ClassifierDataset, self).__init__(file, look_back=look_back, look_ahead=look_ahead, norm=norm,
                                                limit=limit)
        self.gap = gap
        self.feature_engineer = feature_engineer

    def __getitem__(self, item):
        idx = item + self.look_back
        input = self.data[item:idx]
        gt = self.data[idx:idx + self.look_ahead]

        # take  9 features, except close & open time
        feature_idx = SELECTED_FEATURE_IDX

        input = np.array(input, dtype=np.float32)
        input = input[:, feature_idx]

        # take  9 features, except close & open time

        gt = np.array(gt, dtype=np.float32)
        gt = gt[:, feature_idx]

        event = 0.0 if gt[-1, 3].item() < input[-1, 3].item() else 1.0

        if self.feature_engineer is not None:
            input = self.feature_engineer(input)

        # p_mean = input[:, 0:4].mean()
        # p_std = input[:, 0:4].std()
        mean = input.mean(axis=0)
        std = input.std(axis=0)
        # mean[0:4] = p_mean
        # std[0:4] = p_std
        input = (input - mean) / std
        #gt = (gt - mean) / std

        return {
            "input": input,  # Lb x 9,
            "mean": mean,
            "std": std,
            "ahead": gt,  # La x 9
            "event": event
        }

    def __len__(self):
        return len(self.data) - self.look_back - self.look_ahead + 1
