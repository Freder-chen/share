# -*- coding: utf-8 -*-

import pandas as pd
from ..util.common import check_date
from ..models import TushareproBaseModel, TushareproTradeDateModel, TushareproHistoryModel
from ..piplines import TushareProBasePipeline, TushareProTradeDatePipline, TushareProHistoryPipeline


__all__ = [
    'download',
    'download_base', 'download_trade_date', 'download_history',
    'drop_table', 'drop_base_table', 'drop_trade_date_table', 'drop_history_table',
    'is_open', 'have_open', 'get_all_symbols', 'get_stocks_base', 'get_daily'
]

# about datebase #

def download_base():
    TushareProBasePipeline().save()


def download_trade_date():
    TushareProTradeDatePipline().save()


def download_history():
    TushareProHistoryPipeline().save()


def download():
    print('The interface is outdated...')
    download_base()
    download_history()


def drop_base_table():
    if TushareproBaseModel.table_exists():
        TushareproBaseModel.drop_table()


def drop_trade_date_table():
    if TushareproTradeDateModel.table_exists():
        TushareproTradeDateModel.drop_table()

def drop_history_table():
    if TushareproHistoryModel.table_exists():
        TushareproHistoryModel.drop_table()


def drop_table():
    drop_base_table()
    drop_trade_date_table()
    drop_history_table()

# end of datebase #


# about getting data #

def is_open(date):
    return TushareproTradeDateModel[check_date(date)].is_open


def have_open(start_date, end_date):
    query = TushareproTradeDateModel.select().where(
        (TushareproTradeDateModel.date >= check_date(start_date)) &
        (TushareproTradeDateModel.date <= check_date(end_date))
    )
    return True in [item['is_open'] for item in query.dicts()]


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
    if start_date is not None:
        query = query.where(TushareproHistoryModel.trade_date >= check_date(start_date))
    if end_date is not None:
        query = query.where(TushareproHistoryModel.trade_date <= check_date(end_date))
    return pd.DataFrame(list(query.dicts()))

# end of getting data #
