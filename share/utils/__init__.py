# -*- coding: utf-8 -*-

# import functools
import os
import time
import json
import logging
import requests
from abc import abstractmethod, ABCMeta
from ..config import User_Agent, ERROR_PATH


# def get_mean(df, n):
#     return df['close'].rolling(n).mean().shift(1-n)


def _get_user_agent():
    return User_Agent


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

    def __init__(self, delay=1, log_path=ERROR_PATH, log_level=logging.WARNING):
        super(BaseSpider, self).__init__()
        # for log
        self._log_path  = log_path
        self._log_level = log_level
        self.set_logger()
        # for request
        self._delay     = delay
        self._request   = requests.Session()
        self._request.headers['User-Agent'] = _get_user_agent()

    def set_logger(self, log_path=None, log_level=None):
        self._logger = BaseLogger.get_file_logger(
            self.name,
            log_path  or self._log_path,
            log_level or self._log_level,
        )

    def get_raw(self, url, timeout=10, times=3):
        if times == 0:
            return None
        try:
            time.sleep(self._delay)
            return self._request.get(url, timeout=timeout)
        except Exception as e:
            self._logger.error('get_raw error: {}'.format(e))
            return self.get_raw(url, timeout=timeout, times=times-1)

    def request(self, url):
        try:
            self._logger.debug('request url: {}'.format(url))
            return self.get_raw(url)
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
        from http.client import HTTPResponse
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
    name   = 'base_pipline'
    spider = None
    model  = None
    crawl_item_num = 0

    def __init__(self, log_path=ERROR_PATH):
        super(BasePipline, self).__init__()
        self._log_path  = log_path
        self._log_level = logging.WARNING
        self.set_logger()

    def set_logger(self, log_path=None, log_level=None):
        self._logger = BaseLogger.get_file_logger(
            self.name,
            log_path or self._log_path,
            log_level or self._log_level,
        )

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
        for item in self.spider.do_spider():
            self.process_item(item)


class DoFuncItem(object):

    def __init__(self, name, level, func):
        super(DoFuncItem, self).__init__()
        self.name  = name
        self.level = DoFuncItem._check_level(level)
        self.func  = DoFuncItem._check_func(func)

    @staticmethod
    def _check_level(level):
        if isinstance(level, int):
            return level
        # else
        raise TypeError('level not an integer: {}'.format(level))

    @staticmethod
    def _check_func(func):
        from collections import Callable
        if isinstance(func, Callable):
            return func
        # else
        raise TypeError('func can not call: {}'.format(func))

    def __repr__(self):
        return '{} (name: {}): [level: {}] <func: {}>'.format(self.__class__, self.name, self.level, self.func)

    def __str__(self):
        return self.__repr__
