# -*- coding: utf-8 -*-

# import functools
import os, time, json, logging

import requests
from datetime import datetime
from abc import abstractmethod, ABCMeta
from http.client import IncompleteRead, HTTPResponse

from .setting import User_Agent, ERROR_PATH

# def get_mean(df, n):
#     return df['close'].rolling(n).mean().shift(1-n)


def _get_user_agent():
    return User_Agent


# def get_date(sdate, format='%Y%m%d'):
#     return datetime.strptime(sdate, format)
# def get_today(format='%Y%m%d'):
#     return datetime.now().strftime(format)


def check_date(date):
    import datetime
    if isinstance(date, datetime.date):
        return date.strftime('%Y%m%d')
    elif str(date) == date:
        if len(date) != 8:
            raise ValueError('Unknown date: {}'.format(date))
        return date
    else:
        raise TypeError('date is not datetime.date or a valid string: {}'.format(date))


def query_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def add_folder(spath, foder_name):
    path = '{}/{}'.format(spath, foder_name)
    query_folder(path)
    return path


class BaseLogger(object):

    @staticmethod
    def get_file_logger(name, log_path, level, format='%(asctime)s %(name)s : [%(levelname)s] %(message)s'):
        query_folder(os.path.dirname(log_path))

        handler = logging.FileHandler(filename=log_path)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(format))
        
        logger = logging.getLogger(name)
        logger.addHandler(handler)
        return logger


class BaseSpider(metaclass=ABCMeta):
    name = 'base_spider'
    urls = []

    def __init__(self, delay=1, log_path=ERROR_PATH):
        super(BaseSpider, self).__init__()
        self._delay   = delay
        self._logger  = BaseLogger.get_file_logger(self.name, ERROR_PATH, logging.WARNING)
        self._request = requests.Session()
        self._request.headers['User-Agent'] = _get_user_agent()

    def get_raw(self, url, timeout=10, times=3):
        if times == 0:
            return None
        try:
            time.sleep(self._delay)
            return self._request.get(url, timeout=timeout)
        except Exception as e:
            self._logger.error(e)
            return self.get_raw(url, timeout=timeout, times=times - 1)

    def get(self, url, timeout=10, times=3):
        raw = self.get_raw(url, timeout=timeout, times=times)
        if raw:
            return raw
        return None

    def request(self, url, type=None):
        try:
            self._logger.debug('request url: {}'.format(url))
            return self.get(url)
        except Exception as e:
            self._logger.error('request error: {}'.format(e))
            return None

    def url_generator(self):
        for url in self.urls:
            yield url

    def start_requests(self):
        for url in self.url_generator():
            response = self.request(url)
            if response:
                yield response
    
    @abstractmethod
    def parse(self, response):
        raise NotImplementedError("You need to implement this method 'parse'.")

    def do_spider(self):
        for response in self.start_requests():
            try:
                for item in self.parse(response):
                    self._logger.debug('scraped item: {}'.format(item))
                    yield item
            except Exception as e:
                if type(response) is HTTPResponse:
                    self._logger.error('parse error <{}>\n    {}'.format(response.geturl(), e))
                else:
                    self._logger.error('parse error: {}'.format(e))


class BasePipline(metaclass=ABCMeta):
    name = 'base_pipline'
    spider = None
    model = None
    crawl_item_num = 0

    def __init__(self, log_path=ERROR_PATH):
        super(BasePipline, self).__init__()
        self._logger = BaseLogger.get_file_logger(self.name, log_path, logging.WARNING)

    def create_item(self, item):
        self.model.create(**item)

    def process_item(self, item):
        try:
            self.crawl_item_num += 1
            self._logger.info('create {} item: {}'.format(self.crawl_item_num, item))
            self.create_item(item)
        except Exception as e:
            if type(e.args) is tuple and len(e.args) > 1 and e.args[0] == 1062:
                self._logger.warning('have duplicate data: {}'.format(item))
            else:
                self._logger.error(e)
    
    def save(self):
        if not self.model.table_exists():
            self.model.create_table()
        # with db.atomic():
        for item in self.spider.do_spider():
            self.process_item(item)


class DoFuncItem(object):

    def __init__(self, name, level, func=None):
        super(DoFuncItem, self).__init__()
        self.name  = name
        self.level = level
        self.func  = func

    @staticmethod
    def _check_level(level):
        if isinstance(level, int):
            l = level
        else:
            raise TypeError('level not an integer: {}'.format(level))
        return l

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.level >= other.level
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.level > other.level
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.level <= other.level
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.level < other.level
        return NotImplemented
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.level == other.level
        return NotImplemented

    def __ne__(self, other):
        if self.__class__ is other.__class__:
            return self.level != other.level
        return NotImplemented

    def __repr__(self):
        return '{} (name: {}): [level: {}] <func: {}>'.format(self.__class__, self.name, self.level, self.func)

    def __str__(self):
        return self.__repr__
