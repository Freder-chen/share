# -*- coding: utf-8 -*-

import datetime
from .util.common import BasePipline
from .models import db, TushareproBaseModel, TushareproHistoryModel, XueqiuModel, EastMoneyModel


__all__ = ['TushareProBasePipeline', 'TushareProHistoryPipeline', 'XueqiuPipeline', 'EastMoneyPipeline']
        

class TushareProBasePipeline(BasePipline):
    name   = 'tusharepro_base_pipeline'

    def __init__(self):
        from .spiders.tusharepro import TushareProBaseSpider
        super(TushareProBasePipeline, self).__init__()
        self.spider = TushareProBaseSpider(delay=0.3)
        self.model  = TushareproBaseModel

    def create_item(self, item):
        self.model.create(**item)

    def save(self):
        if self.model.table_exists():
            self.model.drop_table()
        if not self.model.table_exists():
            self.model.create_table()
        with db.atomic():
            for item in self.spider.do_spider():
                self.process_item(item)


class TushareProHistoryPipeline(BasePipline):
    from .spiders.tusharepro import TushareProHistorySpider

    name   = 'tusharepro_history_pipeline'
    spider = TushareProHistorySpider(delay=0.3)
    model  = TushareproHistoryModel


class XueqiuPipeline(BasePipline):
    name   = 'xueqiu_pipeline'

    def __init__(self):
        from .spiders.xueqiu import XueqiuSpider
        super(XueqiuPipeline, self).__init__()
        self.spider = XueqiuSpider(delay=1.5)
        self.model  = XueqiuModel
        self._today  = datetime.date.today()

    def create_item(self, item):
        # item = { k: v for k, v in item.items() if k in [
        #     'symbol', 'dividend_yield', 'turnover_rate', 'xq_followers', 'pb', 'current'
        # ]}
        item['date'] = self._today
        self.model.create(**item)


class EastMoneyPipeline(BasePipline):
    name = 'east_money_pipeline'

    def __init__(self):
        from .spiders.eastmoney import EastMoneySpider
        super(EastMoneyPipeline, self).__init__()
        self.spider = EastMoneySpider(delay=0.9)
        self.model = EastMoneyModel
        self._today  = datetime.date.today()

    def create_item(self, item):
        item['date'] = self._today
        self.model.create(**item)