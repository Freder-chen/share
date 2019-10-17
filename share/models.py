# -*- coding: utf-8 -*-

from peewee import *
from .config import MYSQL_HOST, MYSQL_PORT, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWD, MYSQL_CHARSET

# mysql -u root -e "create database share"; 
# mysql -u root -p
# create database share;


db = MySQLDatabase(MYSQL_DBNAME, host=MYSQL_HOST, port=MYSQL_PORT,
    user=MYSQL_USER, passwd=MYSQL_PASSWD, charset=MYSQL_CHARSET)


class BaseModel(Model):
    class Meta:
        database = db


class TushareproBaseModel(BaseModel):
    symbol    = CharField(max_length=10, primary_key=True, null=False)
    name      = CharField(max_length=20, null=True)
    area      = CharField(max_length=20, null=True)
    industry  = CharField(max_length=20, null=True)
    list_date = CharField(max_length=15, null=True)

    class Meta:
        table_name = 'tusharepro_base'
        # primary_key = 'symbol'


class TushareproTradeDateModel(BaseModel):
    date    = DateField(primary_key=True, null=False)
    is_open = BooleanField(null=False)

    class Meta:
        table_name = 'tusharepro_trade_date'        


class TushareproHistoryModel(BaseModel):
    symbol     = CharField(max_length=10, null=False)
    trade_date = DateField(null=False)
    open       = FloatField(null=True)
    high       = FloatField(null=True)
    low        = FloatField(null=True)
    close      = FloatField(null=True)
    pre_close  = FloatField(null=True)
    change     = FloatField(null=True)
    pct_chg    = FloatField(null=True)
    vol        = FloatField(null=True)
    amount     = FloatField(null=True)

    class Meta:
        table_name = 'tusharepro_history'
        primary_key = CompositeKey('symbol', 'trade_date')


class XueqiuModel(BaseModel):
    symbol         = CharField(max_length=10, null=False)
    date           = DateField(null=False)
    current        = FloatField(null=True)
    pb             = FloatField(null=True)
    dividend_yield = FloatField(null=True)
    turnover_rate  = FloatField(null=True)
    xq_followers   = FloatField(null=True)

    class Meta:
        table_name = 'xueqiu'
        primary_key = CompositeKey('symbol', 'date')


class EastMoneyModel(BaseModel):
    symbol                         = CharField(max_length=10, null=False)
    date                           = DateField(null=False)
    next_day_sample_num            = FloatField(null=True)
    next_day_rose_probability      = FloatField(null=True)
    next_day_chg_avg               = FloatField(null=True)
    next_five_day_sample_num       = FloatField(null=True)
    next_five_day_rose_probability = FloatField(null=True)
    next_five_day_chg_avg          = FloatField(null=True)
    total_score                    = FloatField(null=True)
    capital_score                  = FloatField(null=True)
    value_score                    = FloatField(null=True)
    market_heat_score              = FloatField(null=True)
    focus_score                    = FloatField(null=True)
    msg_count                      = FloatField(null=True)
    stock_focus                    = FloatField(null=True)
    stock_focus_chg                = FloatField(null=True)
    people_num_chg                 = FloatField(null=True)
    five_day_avg_buy_price         = FloatField(null=True)
    avg_pos_rate                   = FloatField(null=True)

    class Meta:
        table_name = 'east_money'
        primary_key = CompositeKey('symbol', 'date')


class HistoryRateModel(BaseModel):
    symbol            = CharField(max_length=10, primary_key=True, null=False)
    name              = CharField(max_length=20, null=True)
    area              = CharField(max_length=20, null=True)
    industry          = CharField(max_length=20, null=True)
    current           = FloatField(null=True)
    dividend_yield    = FloatField(null=True)
    turnover_rate     = FloatField(null=True)
    rate              = FloatField(null=True)
    xq_followers      = FloatField(null=True)
    focus_score       = FloatField(null=True)
    market_heat_score = FloatField(null=True)
    stock_focus       = FloatField(null=True)

    class Meta:
        table_name = 'history_rate'
