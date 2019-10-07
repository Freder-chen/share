# -*- coding: utf-8 -*-

from .tusharepro import (
    get_all_symbols as get_ts_all_symbols,
    get_stocks_base as get_ts_stocks_base,
    get_daily as get_ts_daily,
    download_base as download_ts_base,
    download_trade_date as download_ts_trade_date,
    download_history as download_ts_history,
    drop_base_table as drop_ts_base_table,
    drop_trade_date_table as drop_ts_trade_date_table,
    drop_history_table as drop_ts_history_table,
    is_open as is_ts_open,
    have_open as have_ts_open
)

from .xueqiu import (
    get_stocks_base as get_xq_stocks_base,
    download as download_xq,
    drop_table as drop_xq_table
)

from .eastmoney import (
    get_stock_comment as get_em_stock_comment,
    download as download_em,
    drop_table as drop_em_table
)

from ..util.common import DoFuncItem


__all__ = [
    'update', 'download', 'drop_tables', 'is_open', 'have_open',
    'get_all_symbols', 'get_stocks_base', 'get_daily',
    'get_xq_feature', 'get_em_feature'
]


_update_enum = [
    DoFuncItem(name='TushareProBase',      level=10, func=download_ts_base),
    DoFuncItem(name='TushareProTradeDate', level=10, func=download_ts_trade_date),
    DoFuncItem(name='TushareProHistory',   level=20, func=download_ts_history),
    DoFuncItem(name='EastMoney',           level=20, func=download_xq),
    DoFuncItem(name='XueQiu',              level=20, func=download_em),
]

_drop_enum = [
    DoFuncItem(name='TushareProBase',      level=10, func=drop_ts_base_table),
    DoFuncItem(name='TushareProTradeDate', level=10, func=drop_ts_trade_date_table),
    DoFuncItem(name='TushareProHistory',   level=10, func=drop_ts_history_table),
    DoFuncItem(name='EastMoney',           level=10, func=drop_xq_table),
    DoFuncItem(name='XueQiu',              level=10, func=drop_em_table),
]


def _check_dofunc_item(dofunc_item, enum):
    kw = {item.name: item for item in enum}
    if isinstance(dofunc_item, DoFuncItem):
        if dofunc_item.name not in kw.keys():
            raise ValueError('Unknown dofunc_item: {}'.format(dofunc_item))
        di = kw[dofunc_item.name]
    elif str(dofunc_item) == dofunc_item:
        if dofunc_item not in kw.keys():
            raise ValueError('Unknown dofunc_item: {}'.format(dofunc_item))
        di = kw[dofunc_item]
    else:
        raise TypeError('dofunc_item is not a DoFuncItem or a valid string: {}'.format(dofunc_item))
    return di


def _check_dofunc_list(dofunc_list, enum):
    if type(dofunc_list).__name__ in ['list', 'set', 'tuple']:
        l = [_check_dofunc_item(t, enum) for t in dofunc_list]
    elif str(dofunc_list) == dofunc_list:
        l = [_check_dofunc_item(dofunc_list, enum)]
    else:
        raise TypeError('dofunc_list not a list, a set or a valid string: {}'.format(dofunc_list))
    return l


def update(update_list=_update_enum):
    l = _check_dofunc_list(update_list, _update_enum)
    l.sort(key=lambda x: x.level)
    for i in l:
        i.func()


def download(update_list=_update_enum):
    update(update_list)


def drop_tables(drop_list=_drop_enum):
    l = _check_dofunc_list(drop_list, _drop_enum)
    l.sort(key=lambda x: x.level)
    for i in l: i.func()


def is_open(date):
    return is_ts_open(date)


def have_open(start_date, end_date):
    return have_ts_open(start_date, end_date)


def get_all_symbols():
    return get_ts_all_symbols()


def get_stocks_base():
    return get_ts_stocks_base()


def get_daily(symbol, start_date=None, end_date=None):
    return get_ts_daily(symbol, start_date, end_date)


def get_xq_feature():
    return get_xq_stocks_base()


def get_em_feature():
    return get_em_stock_comment()

