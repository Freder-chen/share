# -*- coding: utf-8 -*-

import json
from ..util.common import BaseSpider
from ..api.tusharepro import get_all_symbols


__all__ = ['EastMoneySpider']


def _trans_var(vstr):
    def _trans_generator(vstr):
        yield vstr[0].lower()
        for c in vstr[1:]:
            yield '_{}'.format(c.lower()) if c.isupper() else c 
    return ''.join([c for c in _trans_generator(vstr)])


def _trans_dict(rdict, keys=None):
    if keys is not None:
        rdict = { k: rdict[k] for k in keys }
    return { _trans_var(k): v for k, v in rdict.items() }


def _check_result(res):
    if res and 'HasError' in res and res['HasError'] == False:
        return res['Scode'][:6], res['ApiResults']
    # else
    raise Exception('east money request has error, res: {}'.format(res))


class EastMoneySpider(BaseSpider):
    name = 'eastmoney_spider'

    def url_generator(self):
        for symbol in get_all_symbols():
            yield 'http://data.eastmoney.com/stockcomment/API/{}.json'.format(symbol)

    def parse(self, response):
        try:
            symbol, jdata = _check_result(json.loads(response.content.decode('utf-8')))
        except Exception as e:
            raise Exception(e)
        item = { 'symbol': symbol }
        item.update(_trans_dict(jdata['zhpj']['RiseAndFallPredict'][0]))
        item.update(_trans_dict(jdata['zhpj']['ComprehensiveReview'][0], keys=['TotalScore', 'MsgCount', 'CapitalScore', 'ValueScore']))
        item.update(_trans_dict(jdata['scrd']['summary'][0], keys=['StockFocus', 'StockFocusChg', 'PeopleNumChg', 'FiveDayAvgBuyPrice', 'AvgPosRate', 'MarketHeatScore']))
        item.update(_trans_dict(jdata['zj']['Market'][0], keys=['FocusScore']))
        yield item
