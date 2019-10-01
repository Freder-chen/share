# -*- coding: utf-8 -*-

import time
import datetime
import tushare as ts
from peewee import fn
from ..util.setting import TUSHAREPRO_TOKEN
from ..util.common import BaseSpider
from ..models import TushareproBaseModel, TushareproHistoryModel


__all__ = ['pro', 'TushareProBaseSpider', 'TushareProHistorySpider']


pro = ts.pro_api(TUSHAREPRO_TOKEN)


class TushareProBaseSpider(BaseSpider):
    name = 'tusharepro_base_spider'

    def start_requests(self):
        yield pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

    def parse(self, respose):
        for item in respose.to_dict('records'):
            yield item


class TushareProHistorySpider(BaseSpider):
    name = 'tusharepro_history_spider'

    def _get_daily(self, symbol, start=None, end=None):
        def _get_ts_code(symbol):
            signd = { 'SZ': ['000', '001', '002', '300'], 'SH': ['600', '601', '603', '688'] }
            for capital, codes in signd.items():
                if symbol[:3] in codes:
                    return '{}.{}'.format(symbol, capital)
            return None

        while True:
            try:
                time.sleep(self._delay)
                return pro.daily(ts_code=_get_ts_code(symbol), start_date=start, end_date=end)
            except ConnectionError:
                continue
            except Exception as e:
                self._logger.warning('{}: {}'.format(symbol, e))
                return None
    
    @staticmethod
    def _get_all_symbol():
        query = TushareproBaseModel.select(TushareproBaseModel.symbol)
        return [item['symbol'] for item in query.dicts()]

    @staticmethod
    def _find_daily(symbol):
        query = TushareproHistoryModel.select().where(TushareproHistoryModel.symbol == symbol)
        if not query: return None
        return TushareproHistoryModel.select(fn.MAX(TushareproHistoryModel.trade_date)).where(TushareproHistoryModel.symbol == symbol).scalar()

    def start_requests(self):
        for symbol in TushareProHistorySpider._get_all_symbol():
            start = TushareProHistorySpider._find_daily(symbol)
            if start:
                start += datetime.timedelta(days=1)
                end = datetime.date.today()
                if start < end:
                    yield self._get_daily(symbol=symbol, start=start.strftime('%Y%m%d'))
            else:
                yield self._get_daily(symbol=symbol)

    def parse(self, respose):
        for item in respose.to_dict('records'):
            item['ts_code'] = item['ts_code'][:6]
            item['symbol'] = item.pop('ts_code', None)
            yield item
