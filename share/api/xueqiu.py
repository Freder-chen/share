# -*- coding: utf-8 -*-

import pandas as pd
from peewee import fn
from ..utils import check_date
from ..models import XueqiuModel
from ..piplines import XueqiuPipeline


__all__ = ['download', 'drop_table', 'get_stocks_base']


def download():
    XueqiuPipeline().save()


def drop_table():
    if XueqiuModel.table_exists():
        XueqiuModel.drop_table()


def get_stocks_base(symbol=None, start_date=None, end_date=None):
    query = XueqiuModel.select()
    # TO-DO: warning have no data
    if symbol:
        query = query.where(XueqiuModel.symbol == symbol)
    if start_date:
        query = query.where(XueqiuModel.date >= check_date(start_date))
    if end_date:
        query = query.where(XueqiuModel.date <= check_date(end_date))
    return pd.DataFrame(list(query.dicts()))
