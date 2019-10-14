# -*- coding: utf-8 -*-

try:
    import setting
except ImportError:
    setting = object()


def _getattr(name, default=None, t=str):
    ret = getattr(setting, name, default)
    if isinstance(ret, t):
        return ret
    # else
    raise TypeError('the param {} is not {}: {}'.format(name, t.__name__, ret))


'''
for log
'''
import os, sys
ERROR_PATH = _getattr('ERROR_PATH', os.path.join(sys.path[0], 'log', 'error.out'), str)


'''
for request
'''
User_Agent = _getattr('User_Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36', str)


'''
for mysql
'''
MYSQL_HOST    = _getattr('MYSQL_HOST',    'localhost',   str)
MYSQL_PORT    = _getattr('MYSQL_PORT',     3306,         int)
MYSQL_DBNAME  = _getattr('MYSQL_DBNAME',  'share',       str)
MYSQL_USER    = _getattr('MYSQL_USER',    'root',        str)
MYSQL_PASSWD  = _getattr('MYSQL_PASSWD',  'your passwd', str)
MYSQL_CHARSET = _getattr('MYSQL_CHARSET', 'utf8',        str)


'''
for xueqiu
'''


'''
for tushare pro
'''
# from https://tushare.pro/register?reg=233504
TUSHAREPRO_TOKEN = _getattr('TUSHAREPRO_TOKEN', 'your token')


'''
for eastmoney
'''
