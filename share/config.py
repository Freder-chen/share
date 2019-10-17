# -*- coding: utf-8 -*-

import os, sys


default_config = {
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


def import_string(import_name):
    try:
        __import__(import_name)
    except ImportError:
        # if "." not in import_name:
        raise
    else:
        return sys.modules[import_name]


def config_by_object(obj):
    if isinstance(obj, str):
        obj = import_string(obj)
    for key in dir(obj):
        if key.isupper():
            setattr(sys.modules[__name__], key, getattr(obj, key))


for key, value in default_config.items():
    setattr(sys.modules[__name__], key, value)

config_by_object('setting')
