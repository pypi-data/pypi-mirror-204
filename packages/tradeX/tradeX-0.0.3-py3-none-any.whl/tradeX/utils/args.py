import argparse


def make_parser():
    parser = argparse.ArgumentParser("Base parser for tradeX experiments")
    parser.add_argument("--train_data", default="data/BTCUSDT_1m_train.json", type=str,
                        help="Path to train data file")
    parser.add_argument("--val_data", default="data/BTCUSDT_1m_val.json", type=str,
                        help="Path to val data file")
    parser.add_argument("--exp", default="default", help="name of the experiment")
    parser.add_argument("--epochs", type=int, default=1000, help="max epochs to train")
    parser.add_argument("--lr", type=float, default=0.01, help="learning rate, default 0.01")
    parser.add_argument("--bsize", type=int, default=8, help="batch size, default 8")

    parser.add_argument("--norm", choices=["True", "False"],
                        help="norm input data or not (gaussian norm)")
    parser.add_argument("-lb", "--look_back", type=int, default=1000, help="length of input sequence (look back)")
    parser.add_argument("-la", "--look_ahead", type=int, default=5,
                        help="length of data sequence a head to examine (look ahead)")
    parser.add_argument("-g", "--gap", type=float, default=40, help="gap to determine bumb/dump")

    parser.add_argument("--ckpt_dir", default="weights", help="Directory to save checkpoint")
    parser.add_argument("--log_dir", default="logs", help="Directory to log training.")
    parser.add_argument("--num_gpus", type=int, default=1)
    parser.add_argument("--num_workers", type=int, default=4)
    return parser
