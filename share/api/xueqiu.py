# -*- coding: utf-8 -*-

import pandas as pd
from peewee import fn
from ..models import XueqiuModel
from ..piplines import XueqiuPipeline


__all__ = ['download', 'drop_table', 'get_all_symbols', 'get_stocks_base']


def download():
    XueqiuPipeline().save()


def drop_table():
    if XueqiuModel.table_exists():
        XueqiuModel.drop_table()


def get_stocks_base():
    query = XueqiuModel.select().where(
        XueqiuModel.date == XueqiuModel.select(fn.MAX(XueqiuModel.date)).scalar()
    )
    return pd.DataFrame(list(query.dicts()))[['symbol', 'current', 'pb', 'dividend_yield', 'turnover_rate', 'xq_followers']]
