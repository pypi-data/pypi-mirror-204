import os
import time
from concurrent.futures import ThreadPoolExecutor
import pandas
import requests
import ast

from pandas import DataFrame
from tacv.fileUtils import save_json, get_all_files, load_json
from loguru import logger


def get_backtest_data(symbol, dfrom, dto, interval, save_path):
    assert dfrom < dto
    if dfrom <= 1638327420000:
        logger.warning("Data before that time was used to train, backtest will not be reliable.")
    dir = os.path.dirname(save_path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    all_data = []
    total_time = dto - dfrom
    chunk = _get_data_chunk(symbol, dfrom=dfrom, interval=interval)
    start_time = time.time() * 1000
    while chunk is not None:
        if len(chunk) > 0 and dfrom < dto:
            dfrom = chunk[-1][6] + 1
            chunk = _get_data_chunk(symbol, dfrom=dfrom, interval=interval)
            all_data.extend(chunk)
            end_time = time.time() * 1000
            remaining_percent = (dto - dfrom) / total_time
            remaining_time = (end_time - start_time) / (1 - remaining_percent) * remaining_percent
            logger.info(f"Estimate to finish in {remaining_time / 1000} seconds.")
        else:
            save_json(save_path, all_data)  # save json
            pdata = DataFrame.from_records(all_data, index="OpenTime",
                                           columns=["OpenTime", "Open", "High", "Low", "Close", "Volume", "CloseTime",
                                                    "QuoteVolume", "NumTrades", "TakerBuyVolume", "TakerBuyQuoteVolume",
                                                    "Ignore"])
            pdata.index = pandas.to_datetime(pdata.index, unit='ms')
            pdata = pdata.drop(columns=["CloseTime", "Ignore"]).astype(float)
            DataFrame.to_csv(pdata, save_path.replace("json", "csv"), index=True)
            return pdata
    else:
        print(f"Error when getting data, params: symbol={symbol}, interval={interval},dfrom={dfrom}")

    return all_data


def get_data_all_the_time(symbol, dfrom, interval, save_path):
    if save_path is not None:
        base_name = os.path.basename(save_path)
        dir = os.path.dirname(save_path)
    all_data = []
    chunk = _get_data_chunk(symbol, dfrom=dfrom, interval=interval)
    i = 0
    while chunk is not None:
        if len(chunk) > 0:
            dfrom = chunk[-1][6] + 1
            chunk = _get_data_chunk(symbol, dfrom=dfrom, interval=interval)
            all_data.extend(chunk)
        else:
            # merge data_temp files
            if save_path is not None:
                all_files = get_all_files(dir, recursive=False, exts=["json"])
                all_files = [f for f in all_files if "temp_" in f]
                all_files.sort()
                all_data = []
                for f in all_files:
                    all_data.extend(load_json(f))
                save_json(save_path, all_data)
                print(f"Removing {len(all_files)} file(s).")
                for f in all_files:
                    os.remove(f)
                logger.info("Done getting all data.")
            break

        if i % 10 == 0:
            if save_path is not None:
                logger.info(f"Saving temp data ({len(all_data)} rows)")
                save_json(os.path.join(dir, "temp_" + f"{i}".zfill(10) + base_name), all_data)
                all_data = []
        i += 1
    else:
        print(f"Error when getting data, params: symbol={symbol}, interval={interval},dfrom={dfrom}")
    return all_data


def _get_data_chunk(symbol, dfrom, interval, save_to=None):
    """
    :param symbol: .e.g. BTCUSDT
    :param dfrom: milliseconds since epoch
    :param dto: milliseconds since epoch
    :param interval: 1m, 1h, 1d,...
    :return: json array of trade
    """
    endpoint = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&startTime={dfrom}"
    res = requests.get(endpoint)
    if res.status_code != 200:
        print(f"Error, reason {res.reason}, content {res.content}")
        return None
    else:
        data = ast.literal_eval(res.text)
        if save_to is not None:
            save_json(save_to, data)
        return data
