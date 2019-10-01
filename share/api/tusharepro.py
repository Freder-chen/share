# -*- coding: utf-8 -*-

import pandas as pd
from ..models import TushareproBaseModel, TushareproHistoryModel
from ..piplines import TushareProBasePipeline, TushareProHistoryPipeline


__all__ = [
    'download', 'download_base', 'download_history',
    'drop_table', 'drop_base_table', 'drop_history_table',
    'is_open', 'get_all_symbols', 'get_stocks_base', 'get_daily'
]


def download_base():
    TushareProBasePipeline().save()


def download_history():
    TushareProHistoryPipeline().save()


def download():
    download_base()
    download_history()


def drop_base_table():
    if TushareproBaseModel.table_exists():
        TushareproBaseModel.drop_table()


def drop_history_table():
    if TushareproHistoryModel.table_exists():
        TushareproHistoryModel.drop_table()


def drop_table():
    drop_base_table()
    drop_history_table()


# def get_mean(df, n):
#     return df['close'].rolling(n).mean().shift(1-n)


def is_open(date):
    from ..spiders.tusharepro import pro
    return bool(pro.trade_cal(start_date=date, end_date=date).loc[0, 'is_open'])


def get_all_symbols():
    query = TushareproBaseModel.select(TushareproBaseModel.symbol)
    return [item['symbol'] for item in query.dicts()]


def get_stocks_base():
    # TO-DO: warning db block.
    query = TushareproBaseModel.select()
    return pd.DataFrame(list(query.dicts()))


def get_daily(symbol, start_date=None, end_date=None):
    query = TushareproHistoryModel.select().where(TushareproHistoryModel.symbol == symbol)
    # if query is empty, means there are not exist the symbol.
    # TO-DO: warning
    if type(start_date) is str:
        query = query.where(TushareproHistoryModel.trade_date >= start_date)
    if type(end_date) is str:
        query = query.where(TushareproHistoryModel.trade_date <= end_date)
    return pd.DataFrame(list(query.dicts()))
