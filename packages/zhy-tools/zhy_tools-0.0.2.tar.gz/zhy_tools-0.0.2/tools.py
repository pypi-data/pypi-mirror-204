#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Hongyu Zhao
@contact:zhaohongyu2401@yeah.com
@version: 1.0.0
@file: tools.py
@time: 2023/2/20 18:35
"""
from functools import wraps
import datetime 
import time
 
# time装饰器
def timer(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        begin_time = time.perf_counter()
        result = func(*args, **kwargs)
        start_time = time.perf_counter()
        total = start_time - begin_time
        hour = int(total/3600)
        mint = int( (total%3600)/60  )
        sec =  (total%3600)%60
        
        print('func:%r args:[%r, %r] took: %2.4f hour %2.4f min %2.4f sec' % (func.__name__, args, kwargs,hour,mint,sec))
        return result
 
    return wrap

#基于输入的起始日期 向前遍历region天数
def build_date(init_date,region):
    arr = []
    for i in range(region):
        begin = (datetime.datetime.strptime(init_date,'%Y-%m-%d') -  datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        arr.append(begin)
    return arr 

def last_day():
    return (datetime.datetime.now() - datetime.timedelta(1)).strftime('%Y-%m-%d')
