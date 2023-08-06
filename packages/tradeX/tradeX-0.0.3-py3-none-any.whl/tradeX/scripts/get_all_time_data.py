import argparse
import os.path

from tradeX.utils.data_getter import get_data_all_the_time


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, default="BTCUSDT", help="trading pair, .e.g BTCUSDT")
    parser.add_argument("--dfrom", type=int, default=1567962000000,
                        help="Default = 1567962000000 (September 2019),miliseconds since epoch, start time to get trading data to now")
    parser.add_argument("--interval", type=str, default="3m",
                        help="interval of a trading candle (.e.g 1m, 3m, 1h, 1d, 1w, 1M,...)")
    parser.add_argument("--save_dir", type=str, default="data")
    return parser


if __name__ == "__main__":
    args = make_parser().parse_args()
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    symbol = args.symbol
    dfrom = args.dfrom
    interval = args.interval
    save_path = f"{args.save_dir}/{symbol}_{interval}.json"
    get_data_all_the_time(symbol, dfrom, interval, save_path=save_path)
