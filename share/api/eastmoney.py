# -*- coding: utf-8 -*-

import pandas as pd
from peewee import fn
from ..models import EastMoneyModel
from ..piplines import EastMoneyPipeline


__all__ = ['download', 'drop_table', 'get_stock_comment']


def download():
    EastMoneyPipeline().save()


def drop_table():
    if EastMoneyModel.table_exists():
        EastMoneyModel.drop_table()


def get_stock_comment():
    query = EastMoneyModel.select().where(
        EastMoneyModel.date == EastMoneyModel.select(fn.MAX(EastMoneyModel.date)).scalar()
    )
    return pd.DataFrame(list(query.dicts())).drop('date', axis=1)
