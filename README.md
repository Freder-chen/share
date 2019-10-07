# Share

Share 是自己玩股票的小工具，目前还只有爬虫代码，爬取了 tushare、雪球、东方财富的某些特定信息。上传以后方便自己服务器迭代版本。如果能够对其他人有用那也不错。

## 安装

本项目用 Python3 编写，数据库使用 MySQL。只给出linux和OS X的安装命令。

- [Windows Python3安装-菜鸟教程](https://www.runoob.com/python3/python3-install.html)

- [Windows MySQL安装-菜鸟教程](https://www.runoob.com/mysql/mysql-install.html)

```shell
# python environment on linux
apt-get install python3
apt-get install python3-pip
# python environment on Mac
brew install python3

# mysql environment on linux
apt install mysql-server
# mysql environment on Mac
brew install mysql

# 安装需要的python包
python3 -m pip install pymysql pandas peewee tushare requests

# 创建数据库
mysql -uroot -e "create database share" # 可以在 /share/util/setting.py 的 MYSQL_DBNAME 字段中更改数据库名
```

## 部分功能及使用

由于这个项目很大程度上是自用，所以并没有完整的注释和文档。

### 爬取数据导入数据库

```python
'''在爬取数据之前你需要在 /share/util/setting.py 中更改自己的 tushare_pro_token 和数据库密码'''
import share, logging
logging.basicConfig(level=logging.INFO)
share.download()
# 也可以使用 share.update()
```

### 删除数据库数据

```python
import share
share.drop_tables()
```

### 获取数据接口

```python
'''数据接口需要在 share.download() 爬取完成以后才能调用。'''

import share

# True 为交易日，False 为非交易日
bool = share.is_open(date)

# True 为有交易日，False 为无交易日
bool = share.have_open(start_date, end_date)

# 返回深沪两市所有股票代码
list = share.get_all_symbols() 

# 返回深沪两市所有股票基本信息
df = share.get_stocks_base()

# 得到深沪两市某支股票的历史交易信息，start_data和end_date为可选项，格式为‘YYYYMMDD’
df = share.get_daily(symbol, start_date, end_date)

# 得到雪球上的某些特征，如股票关注人数等
df = share.get_xq_feature()

# 得到东方财富的某些特征，如关注热度等
df = share.get_em_feature()
```

