# -*- coding: utf-8 -*-

import pandas as pd
from peewee import fn
from ..utils import check_date
from ..models import EastMoneyModel
from ..piplines import EastMoneyPipeline


__all__ = ['download', 'drop_table', 'get_stock_comment']


def download():
    EastMoneyPipeline().save()


def drop_table():
    if EastMoneyModel.table_exists():
        EastMoneyModel.drop_table()


def get_stock_comment(symbol=None, start_date=None, end_date=None):
    query = EastMoneyModel.select()
    # TO-DO: warning
    if symbol:
        query = query.where(EastMoneyModel.symbol == symbol)
    if start_date:
        query = query.where(EastMoneyModel.date >= check_date(start_date))
    if end_date:
        query = query.where(EastMoneyModel.date <= check_date(end_date))
    return pd.DataFrame(list(query.dicts()))
