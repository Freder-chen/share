# -*- coding: utf-8 -*-

'''
config use like:
    from share import config
    config.ATTRIBUTE
'''


import os, sys
import tushare
from peewee import MySQLDatabase


_default_config = {
    # for log
    'ERROR_PATH':      os.path.join(sys.path[0], 'log', 'error.out'),
    # for request
    'User_Agent':      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
    # for mysql
    'MYSQL_HOST':      'localhost',
    'MYSQL_PORT':      3306,
    'MYSQL_DBNAME':    'share',
    'MYSQL_USER':      'root',
    'MYSQL_PASSWD':    None,
    'MYSQL_CHARSET':   'utf8',
    # for tushare pro
    'TUSHAREPRO_TOKEN': None,
}


def _import_string(import_name):
    try:
        __import__(import_name)
    except ImportError:
        raise
    else:
        return sys.modules[import_name]


def _set_attribute(name, value):
    setattr(sys.modules[__name__], name, value)


def _get_attribute(name):
    getattr(sys.modules[__name__], name)


def set_default_config():
    for key, value in _default_config.items():
        _set_attribute(key, value)


def set_config_by_object(obj):
    if isinstance(obj, str):
        obj = _import_string(obj)
    for key in dir(obj):
        if key.isupper():
            _set_attribute(key, getattr(obj, key))


set_default_config()

try:
    import config
    set_config_by_object(config)
    _set_attribute('PRO', tushare.pro_api(TUSHAREPRO_TOKEN))
    _set_attribute('DB', MySQLDatabase(MYSQL_DBNAME, host=MYSQL_HOST, port=MYSQL_PORT, 
        user=MYSQL_USER, passwd=MYSQL_PASSWD, charset=MYSQL_CHARSET))
except ImportError as e:
    raise



