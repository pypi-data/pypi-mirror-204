import random

import numpy as np
from tacv.fileUtils import load_json
from torch.utils.data import Dataset

from tradeX.datasets.consts import SELECTED_FEATURE_IDX


class RegressionDataset(Dataset):

    def __init__(self, file: str, look_back: int, look_ahead: int = 1, feature_engineer=None):
        self.look_back = look_back
        self.look_ahead = look_ahead
        self.data = load_json(file)
        self.feature_engineer = feature_engineer

    def __getitem__(self, item):
        inp = self.data[item:item + self.look_back]
        gt = self.data[item + self.look_back:item + self.look_back + self.look_ahead]

        # convert to numpy
        inp = np.array(inp)
        gt = np.array(gt)

        # take 9 features, except close & open time
        feature_idx = SELECTED_FEATURE_IDX
        inp = inp[:, feature_idx]  # L_back x 9
        gt = gt[:, feature_idx]  # L_ahead x 9

        # log_return = np.log(gt[-1, 1:4]) - np.log(inp[-1, 1:4])
        log_return_high = np.log(gt[:, 1].max()) - np.log(inp[-1, 1])
        log_return_low = np.log(gt[:, 2].min()) - np.log(inp[-1, 2])
        log_return_close = np.log(gt[-1, 3]) - np.log(inp[-1, 3])
        log_return = np.array((log_return_high, log_return_low, log_return_close))
        if self.feature_engineer is not None:
            inp = self.feature_engineer(inp)

        p_mean = inp[:, 0:4].mean()
        p_std = inp[:, 0:4].std()
        mean = inp.mean(axis=0)
        std = inp.std(axis=0)
        mean[0:4] = p_mean
        std[0:4] = p_std

        if np.count_nonzero(std == 0) != 0:
            return self.__getitem__(random.randint(0, len(self) - 1))

        inp = (inp - mean) / std
        gt = (gt - mean[:9]) / std[:9]

        return {
            "input": inp,  # Lb x 9,
            "mean": mean,
            "std": std,
            "ahead": gt,  # La x 9
            "log_return": log_return,  # 3
        }

    def __len__(self):
        return len(self.data) - self.look_back - self.look_ahead + 1
