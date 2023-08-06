import time
from typing import Union

import numpy as np
import torch

from tradeX.datasets.consts import SELECTED_FEATURE_IDX
from tradeX.utils.data_getter import _get_data_chunk


class DataNormalizer:
    def norm(self, data, *args, **kwargs):
        pass

    def un_norm(self, data, **kwargs):
        pass


class GaussianNormalizer(DataNormalizer):
    def norm(self, data: Union[np.ndarray, torch.Tensor], mean=None, std=None):
        if mean is None or std is None:
            mean = data.mean()
            std = data.std()
        data = (data - mean) / std
        return data, {"mean": mean, "std": std}

    def un_norm(self, data, **kwargs):
        assert "mean" in kwargs and "std" in kwargs, "kwargs must contains mean & std value to decode"
        mean = kwargs["mean"]
        std = kwargs["std"]
        data = data * std + mean
        return data


class MinMaxNormalizer(DataNormalizer):
    def norm(self, data: Union[np.ndarray, torch.Tensor], min=None, max=None):
        if min is None or max is None:
            max = data.max()
            min = data.min()
        data = (data - min) / (max - min)
        return data, {"min": min, "max": max}

    def un_norm(self, data, **kwargs):
        assert "max" in kwargs and "min" in kwargs, "kwargs must contains max min value to decode"
        min = kwargs["min"]
        max = kwargs["max"]
        data = (data + min) * (max - min)
        return data


# def norm_input(input):
#     mms = []
#     normalizer = GaussianNormalizer()
#     for i in range(input.shape[1]):
#         input[:, i], mm = normalizer.norm(input[:, i])
#         mms.append(mm)
#     return input, mms


def un_norm_output(input, mms):
    for i in range(len(input)):
        mean = mms[i]["mean"]
        std = mms[i]["std"]
        input[i] = input[i] * std + mean
    return input


def download_pastdata(symbol, interval, dfrom, save_to):
    data = _get_data_chunk(symbol, dfrom=dfrom, interval=interval, save_to=save_to)
    return data


def download_livedata(symbol, interval):
    data = _get_data_chunk(symbol, dfrom=time.time() * 1000, interval=interval)
    return data


def norm_data(input, gt, norm_gt=True):
    """
    :param input: L x 9
    :param gt: L x 9
    :param norm_gt:
    :return:
    """
    normalizer = GaussianNormalizer()
    ms = []

    price_mean = input[:, 0:4].mean()
    price_std = input[:, 0:4].std()
    for i in range(input.shape[1]):
        if 0 <= i <= 3:
            input[:, i], mm = normalizer.norm(input[:, i], mean=price_mean, std=price_std)
        else:
            input[:, i], mm = normalizer.norm(input[:, i])
        if norm_gt is True:
            gt[:, i], _ = normalizer.norm(gt[:, i], **mm)
        ms.append(mm)
    return input, gt, ms


def process_input(data, window_size, to_torch=True, do_norm=True):
    input = np.array(data, dtype=np.float32)

    # take  9 features, except close & open time
    feature_idx = SELECTED_FEATURE_IDX
    input = input[:, feature_idx]
    mms = None
    if do_norm:
        input, _, mms = norm_data(input, None, norm_gt=False)
    if to_torch:
        input = torch.from_numpy(input).view(window_size, -1).float()
    else:
        # keep numpy
        input = input.reshape(window_size, -1)
    return input, mms


def feature_engineering_volume(in_data: np.ndarray, is_normalized: bool = False):
    """
    :param is_normalized: indicate if the input data is already normalized or not
    :param in_data: L x K for non-batch input or B x L x K for batch input
    :return:  L x K1 for non-batch input or B x L x K1 for batch input
    Where K and K1 are number of features before and after feature engineering
    K = 9
    """
    if is_normalized:
        raise "Feature engineering is now only supports non-normalized data"
    # [open, high, low, close, volume, qv, n, tbbav, tbqav]

    v_and_qv = in_data[..., 4:6]  #
    tbba_tbqa = in_data[..., 7:9]

    unnormed_features = np.concatenate((v_and_qv, tbba_tbqa),
                                       axis=-1)

    mean = unnormed_features.mean()
    std = unnormed_features.std()
    normed_features = (unnormed_features - mean) / std

    return normed_features
