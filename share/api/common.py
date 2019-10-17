# -*- coding: utf-8 -*-

import pandas as pd
from .tusharepro import get_daily, get_stocks_base
from .xueqiu import get_stocks_base as get_xq_feature
from .eastmoney import get_stock_comment as get_em_feature
from ..models import TushareproBaseModel, XueqiuModel, EastMoneyModel, HistoryRateModel

__all__ = ['get_history_rate', 'save_history_rate', 'drop_history_rate']


def _get_daily_mean(df, n):
    return df['close'].rolling(n).mean().shift(1-n)


def _calculat_stocks_cost(symbols):
    rate = []
    for index, symbol in enumerate(symbols):
        df = get_daily(symbol)
        if df is None:
            return None
        try:
            ma5_list = _get_daily_mean(df, 5).dropna().tolist()
            now = ma5_list.pop(0)
            res = sum(map(lambda x: 1 if x < now else 0, ma5_list)) / len(ma5_list)
            rate.append(res)
        except Exception as e:
            print('error: {}, reason: {}'.format(symbol, e))
        print('calculating: {:.2f}%'.format(index / len(symbols) * 100), end='\r')
    return rate


def _select_head(df, col, r=0.2):
    return df.sort_values(col, ascending=False).head(int(df.shape[0] * r))


def _intersect(df, cold):
    indexs = [_select_head(df, col, r).index for col, r in cold.items()]
    # [ch for ch in itertools.ifilter(a.__contains__, b)]
    for i in indexs[1:]:
        indexs[0] = indexs[0].intersection(i)
    return df.loc[indexs[0], :]


def _calculat_history_rate(symbols=None):
    stock_basics = get_stocks_base()[['symbol', 'name', 'area', 'industry']]
    stock_basics = stock_basics.merge(get_xq_feature(), how='left', on='symbol')
    stock_basics = stock_basics.merge(get_em_feature(), how='left', on='symbol')
    stock_basics = _intersect(stock_basics, { k: 0.2  for k in ['xq_followers', 'total_score', 'value_score', 'market_heat_score', 'focus_score', 'stock_focus']})
    stock_basics = stock_basics.loc[(stock_basics['dividend_yield'] > 2) & (stock_basics['turnover_rate'] > 0.5), :]
    if symbols:
        stock_basics = stock_basics[stock_basics['symbol'].isin(symbols)]
        print(stock_basics)
    stock_basics['rate'] = _calculat_stocks_cost(stock_basics['symbol'].tolist())
    stock_basics.sort_values(['rate'], inplace=True)
    stock_basics.reset_index(drop=True, inplace=True)
    return stock_basics[HistoryRateModel._meta.fields.keys()].astype(object).where(pd.notnull(stock_basics), None)


def save_history_rate():
    if HistoryRateModel.table_exists():
        HistoryRateModel.drop_table()
    # if not HistoryRateModel.table_exists():
    HistoryRateModel.create_table()
    for _, item in _calculat_history_rate(['000001', '000002']).iterrows():
        print(item)
        HistoryRateModel.create(**item)


def drop_history_rate():
    if HistoryRateModel.table_exists():
        HistoryRateModel.drop_table()


def get_history_rate(symbols=None):
    query = HistoryRateModel.select()
    return pd.DataFrame(list(query.dicts()))
