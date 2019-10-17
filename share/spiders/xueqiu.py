# -*- coding: utf-8 -*-

import json
from ..utils import BaseSpider


__all__ = ['XueqiuSpider']


def _check_result(res):
    if res and 'error_code' in res and res['error_code'] == 0:
        return res['data']
    # else
    raise Exception(res['error_description'] if res and 'error_description' in res else '')


class XueqiuSpider(BaseSpider):
    name = 'xueqiu_spider'

    def url_generator(self, btypes=['zxb', 'sza', 'sha'], size=30):
        base_url = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size={}&order=desc&order_by=percent&exchange=CN&market=CN&type={}'
        for btype in btypes:
            url = base_url.format(1, size, btype)
            try:
                res = _check_result(json.loads(self.request(url).content.decode('utf-8')))
                total_page = int((res['count'] + size - 1) / size)
            except Exception as e:
                self._logger.exception('get total page fail in <{}>\nerror_description:\n    {}'.format(btype, e))
                continue
            for page in range(1, total_page):
                yield base_url.format(page, size, btype)

    def parse(self, response):
        try:
            items = _check_result(json.loads(response.content.decode('utf-8')))
        except Exception as e:
            raise Exception(e)
        for item in items['list']:
            yield {
                'pb': item['pb'], # 市净率
                'symbol': item['symbol'][2:],
                'current': item['current'], # 现价
                'xq_followers': item['followers'],
                'turnover_rate': item['turnover_rate'], # 换手率
                'dividend_yield': item['dividend_yield'], # 股息率
            }
