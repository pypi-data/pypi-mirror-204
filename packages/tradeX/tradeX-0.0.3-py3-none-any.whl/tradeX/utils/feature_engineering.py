import numpy as np
import talib


def remove_nan(ta_signal: np.array):
    """
    :param ta_signal: K x F
    :return:
    """
    max_nan_index = 0
    max_inf_index = 0
    nan_ids = np.nonzero(np.isnan(ta_signal))[0]
    if len(nan_ids) > 0:
        max_nan_index = nan_ids.max() + 1
    inf_ids = np.nonzero(np.isinf(ta_signal))[0]
    if len(inf_ids) > 0:
        max_inf_index = inf_ids.max() + 1

    cut_idx = max(max_nan_index, max_inf_index)
    return ta_signal[cut_idx:].astype(np.float32)


def feature_engineer_fake(input: np.ndarray):
    """
    :param input: L x 9 where 9 is of ("Open", "High", "Low", "Close", "Vol", "Quote asset volume",
             "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume")
    :param out_seq_length:
    :return:
    """
    """Do nothing, just return"""
    return input


def feature_engineer_20(inp: np.ndarray):
    """("Open", "High", "Low", "Close", "Vol", "Quote asset volume",
             "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume")"""

    inp = inp.astype(float)
    open = inp[:, 0]
    high = inp[:, 1]
    low = inp[:, 2]
    close = inp[:, 3]
    vol = inp[:, 4]
    quote_asset_vol = inp[:, 5]
    num_trades = inp[:, 6]
    tbbav = inp[:, 7]
    tbqav = inp[:, 8]
    sma = talib.SMA(inp[:, 3], timeperiod=10)
    ema = talib.EMA(inp[:, 3], timeperiod=10)
    rsi = talib.RSI(inp[:, 3], timeperiod=14)
    macd, macd_signal, macd_hist = talib.MACD(inp[:, 3], fastperiod=12, slowperiod=26, signalperiod=9)
    stoch_k, stoch_d = talib.STOCH(inp[:, 1], inp[:, 2], inp[:, 3], fastk_period=14, slowk_period=3, slowd_period=3)
    bbands_upper, bbands_middle, bbands_lower = talib.BBANDS(inp[:, 3], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    atr = talib.ATR(inp[:, 1], inp[:, 2], inp[:, 3], timeperiod=14)
    cci = talib.CCI(inp[:, 1], inp[:, 2], inp[:, 3], timeperiod=20)
    obv = talib.OBV(inp[:, 3], inp[:, 4])
    willr = talib.WILLR(inp[:, 1], inp[:, 2], inp[:, 3], timeperiod=14)
    mfi = talib.MFI(inp[:, 1], inp[:, 2], inp[:, 3], inp[:, 4], timeperiod=14)
    roc = talib.ROC(inp[:, 3], timeperiod=10)
    adx = talib.ADX(inp[:, 1], inp[:, 2], inp[:, 3], timeperiod=14)
    trix = talib.TRIX(inp[:, 3], timeperiod=10)
    uo = talib.ULTOSC(inp[:, 1], inp[:, 2], inp[:, 3], timeperiod1=7, timeperiod2=14, timeperiod3=28)
    signals = [open, high, low, close, vol, quote_asset_vol, num_trades, tbbav, tbqav, sma, ema, rsi, macd, macd_signal,
               macd_hist, stoch_k, stoch_d, bbands_upper,
               bbands_middle, bbands_lower, atr, cci, obv, willr, mfi, roc, adx, trix, uo]
    f = np.vstack(signals).T

    # remember to always keep this line to remove NaN values which usually appears in head of each signal
    f = remove_nan(f)
    return f


def feature_engineer_20_half_time_period(inp: np.ndarray):
    """("Open", "High", "Low", "Close", "Vol", "Quote asset volume",
             "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume")"""

    inp = inp.astype(float)
    open = inp[:, 0]
    high = inp[:, 1]
    low = inp[:, 2]
    close = inp[:, 3]
    vol = inp[:, 4]
    quote_asset_vol = inp[:, 5]
    num_trades = inp[:, 6]
    tbbav = inp[:, 7]
    tbqav = inp[:, 8]
    sma = talib.SMA(inp[:, 3], timeperiod=5)
    ema = talib.EMA(inp[:, 3], timeperiod=5)
    rsi = talib.RSI(inp[:, 3], timeperiod=7)
    macd, macd_signal, macd_hist = talib.MACD(inp[:, 3], fastperiod=6, slowperiod=13, signalperiod=5)
    stoch_k, stoch_d = talib.STOCH(inp[:, 1], inp[:, 2], inp[:, 3], fastk_period=7, slowk_period=3, slowd_period=3)
    bbands_upper, bbands_middle, bbands_lower = talib.BBANDS(inp[:, 3], timeperiod=10, nbdevup=2, nbdevdn=2, matype=0)
    atr = talib.ATR(inp[:, 1], inp[:, 2], inp[:, 3], timeperiod=7)
    cci = talib.CCI(inp[:, 1], inp[:, 2], inp[:, 3], timeperiod=10)
    obv = talib.OBV(inp[:, 3], inp[:, 4])
    willr = talib.WILLR(inp[:, 1], inp[:, 2], inp[:, 3], timeperiod=7)
    mfi = talib.MFI(inp[:, 1], inp[:, 2], inp[:, 3], inp[:, 4], timeperiod=7)
    roc = talib.ROC(inp[:, 3], timeperiod=5)
    adx = talib.ADX(inp[:, 1], inp[:, 2], inp[:, 3], timeperiod=7)
    trix = talib.TRIX(inp[:, 3], timeperiod=5)
    uo = talib.ULTOSC(inp[:, 1], inp[:, 2], inp[:, 3], timeperiod1=4, timeperiod2=7, timeperiod3=14)
    signals = [open, high, low, close, vol, quote_asset_vol, num_trades, tbbav, tbqav, sma, ema, rsi, macd, macd_signal,
               macd_hist, stoch_k, stoch_d, bbands_upper,
               bbands_middle, bbands_lower, atr, cci, obv, willr, mfi, roc, adx, trix, uo]
    f = np.vstack(signals).T

    # remember to always keep this line to remove NaN values which usually appears in head of each signal
    f = remove_nan(f)
    return f


def feature_engineer_example(input: np.ndarray):
    """
    :param input: L x 9 where 9 is of ("Open", "High", "Low", "Close", "Vol", "Quote asset volume",
             "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume")
    :param out_seq_length:
    :return:
    """
    # always add this line to convert input to float64
    input = input.astype(float)

    # calculate TA signals
    open = input[:, 0]
    high = input[:, 1]
    low = input[:, 2]
    close = input[:, 3]
    vol = input[:, 4]

    signals = [open, high, low, close]
    signals.append(talib.SMA(close, timeperiod=4))
    signals.append(talib.EMA(close, timeperiod=4))
    signals.append(talib.PLUS_DI(high, low, close, timeperiod=4))

    signals.append(talib.RSI(close, timeperiod=4))
    signals.append(talib.STOCHRSI(close, timeperiod=4))
    signals.append(talib.MA(close, timeperiod=4))
    signals.append(talib.BBANDS(close, timeperiod=4))
    signals.append(talib.MACD(close))
    signals.append(talib.OBV(close, vol))
    signals.append(talib.ADX(high, low, close, timeperiod=4))
    signals.append(talib)
    f = np.vstack(signals).T

    # remember to always keep this line to remove NaN values which usually appears in head of each signal
    f = remove_nan(f)
    return f


def feature_engineer_2(input: np.ndarray):
    """
    :param input: L x 9 where 9 is of ("Open", "High", "Low", "Close", "Vol", "Quote asset volume",
             "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume")
    :param out_seq_length:
    :return:
    """
    # always add this line to convert input to float64
    input = input.astype(float)

    # calculate TA signals
    high = input[:, 1]
    low = input[:, 2]
    close = input[:, 3]
    vol = input[:, 4]
    signals = []
    signals.append(talib.PLUS_DI(high, low, close, timeperiod=4))
    signals.append(talib.EMA(close, timeperiod=4))
    signals.append(talib.RSI(close, timeperiod=4))
    signals.append(talib.STOCHRSI(close, timeperiod=4))
    signals.append(talib.MA(close, timeperiod=4))
    signals.append(talib.BBANDS(close, timeperiod=4))
    signals.append(talib.MACD(close))
    signals.append(talib.OBV(close, vol))
    signals.append(talib.ADX(high, low, close, timeperiod=4))
    f = np.vstack(signals).T

    f = remove_nan(f)
    mean = f.mean(axis=0)
    std = f.std(axis=0)
    f = (f - mean) / std
    return f
