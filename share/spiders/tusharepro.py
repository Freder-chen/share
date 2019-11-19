# -*- coding: utf-8 -*-

import time
import datetime
from peewee import fn
from .. import config
from ..utils import BaseSpider
from ..models import TushareproBaseModel, TushareproTradeDateModel, TushareproHistoryModel

__all__ = ['TushareProBaseSpider', 'TushareProTradeDateSpider', 'TushareProHistorySpider']


# import tushare as ts
# pro = ts.pro_api(config.TUSHAREPRO_TOKEN)


class TushareProBaseSpider(BaseSpider):
    name = 'tusharepro_base_spider'

    def start_requests(self):
        yield config.PRO.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

    def parse(self, respose):
        for item in respose.to_dict('records'):
            yield item


class TushareProTradeDateSpider(BaseSpider):
    name = 'tusharepro_trade_date_spider'

    def start_requests(self):
        try:
            yield config.PRO.trade_cal()
        except Exception as e:
            self._logger.warning(e)

    def parse(self, respose):
        for item in respose.to_dict('records'):
            yield {
                'date':    item['cal_date'],
                'is_open': item['is_open'],
            }


# TushareProHistorySpider #

def _get_signd():
    df = config.PRO.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    df['head'] = df['ts_code'].map(lambda x: x[:3])
    df['tail'] = df['ts_code'].map(lambda x: x[-2:])
    signd = {}
    for _, d in df[['head', 'tail']].drop_duplicates().iterrows():
        signd[d['tail']] = signd.pop(d['tail'], []) + [d['head']]
    return signd # { 'SZ': ['000', ... , '300'], 'SH': ['600', ...] }


def _get_all_symbol():
    query = TushareproBaseModel.select(TushareproBaseModel.symbol)
    return [item['symbol'] for item in query.dicts()]


def _find_daily(symbol):
    query = TushareproHistoryModel.select().where(TushareproHistoryModel.symbol == symbol)
    if not query: return None
    return TushareproHistoryModel.select(fn.MAX(TushareproHistoryModel.trade_date)).where(TushareproHistoryModel.symbol == symbol).scalar()


def _have_work_day(start_date, end_date):
    query = TushareproTradeDateModel.select().where(
        (TushareproTradeDateModel.date >= start_date) &
        (TushareproTradeDateModel.date <= end_date)
    )
    return True in [item['is_open'] for item in query.dicts()]


class TushareProHistorySpider(BaseSpider):
    name = 'tusharepro_history_spider'

    def _get_daily(self, symbol, start=None, end=None):
        def _get_ts_code(symbol):
            for capital, codes in self._signd.items():
                if symbol[:3] in codes:
                    return '{}.{}'.format(symbol, capital)
            return None

        while True:
            try:
                time.sleep(self._delay)
                return config.PRO.daily(ts_code=_get_ts_code(symbol), start_date=start, end_date=end)
            except ConnectionError:
                continue
            except Exception as e:
                self._logger.warning('{}: {}'.format(symbol, e))
                return None

    def start_requests(self):
        self._signd = _get_signd()
        for symbol in _get_all_symbol():
            start = _find_daily(symbol)
            if start:
                start += datetime.timedelta(days=1)
                if _have_work_day(start, datetime.date.today()):
                    yield self._get_daily(symbol=symbol, start=start.strftime('%Y%m%d'))
            else:
                yield self._get_daily(symbol=symbol)

    def parse(self, respose):
        for item in respose.to_dict('records'):
            item['ts_code'] = item['ts_code'][:6]
            item['symbol'] = item.pop('ts_code', None)
            yield item
