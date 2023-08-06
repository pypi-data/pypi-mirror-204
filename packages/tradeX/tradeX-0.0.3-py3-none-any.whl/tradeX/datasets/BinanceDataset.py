import numpy as np
from tacv.fileUtils import load_json
from torch.utils.data import Dataset

from tradeX.datasets.consts import SELECTED_FEATURE_IDX
from tradeX.utils.data import norm_data


class BinanceDataset(Dataset):

    def __init__(self, file: str, look_back: int, look_ahead: int = 1, norm: bool = True, limit: int = -1):
        self.look_back = look_back
        self.look_ahead = look_ahead
        self.data = load_json(file)
        if limit > 0:
            self.data = self.data[:limit]
        self.norm = norm

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

        mm = 0
        if self.norm:
            inp, gt, mm = norm_data(inp, gt, norm_gt=True)

        # input : L_back x 9
        # gt : L_ahead x 9
        return {
            "input": inp,  # L_back x 9
            "gt": gt,  # L_ahead x 9
            "mm": mm if self.norm else 0,  # 9
        }

    def __len__(self):
        return len(self.data) - self.look_back - self.look_ahead + 1
