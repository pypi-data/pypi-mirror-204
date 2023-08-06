from argparse import ArgumentParser
from tacv.fileUtils import load_json, save_json
from tqdm import tqdm
import numpy as np


def make_parser():
    parser = ArgumentParser()
    parser.add_argument("-d", "--data", default="data/BTCUSDT_1m.json", type=str, help="data path json")
    return parser


if __name__ == "__main__":
    args = make_parser().parse_args()
    file = args.data
    data = load_json(file)
    for item in tqdm(data):
        for i in range(len(item)):
            item[i] = float(item[i])
    train_ratio = 0.8
    train_data = data[:int(len(data) * train_ratio)]
    val_data = data[int(len(data) * train_ratio):]

    # just one more step to validate data
    assert np.count_nonzero(np.diff(np.array(train_data)[:, 0]) != 60000) == 0
    assert np.count_nonzero(np.diff(np.array(val_data)[:, 0]) != 60000) == 0
    assert train_data[-1][0] < val_data[0][0]

    save_json(file.replace(".json", "_train.json"), train_data)
    save_json(file.replace(".json", "_val.json"), val_data)
