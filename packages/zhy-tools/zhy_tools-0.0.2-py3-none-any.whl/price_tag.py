#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Hongyu Zhao
@contact:zhaohongyu2401@yeah.com
@version: 1.0.0
@file: price_tag.py
@time: 2022/8/1 14:13
"""
from decimal import Decimal

def round_float(a):
    return float(Decimal(str(a)).quantize(Decimal('.00'), rounding='ROUND_HALF_UP')) # return 4.55


def isfloat(a):
    try:
        a = float(a)
    except:
        return False
    return True 

def load_time_period():
    path = '/root/work_place/zhy/kuaidian/data/feature_data/online_process/sp_period/sp_period.txt'
    
    sp_period = []
    with open(path,'r',encoding='utf8') as f:
        for line in f :
            line = line.strip().split()
            [begin,end,exp] = line 
            sp_period.append(line)
    return sp_period


def load_info():
    data = {}
    count = 0
    with open('/root/anaconda3/lib/python3.8/site-packages/zhy_tool//price_info.txt','r',encoding='utf8') as f :
        for line in f :
            line = line.strip().split()
            count += 1
            if count == 1 : continue
            [prov,month,hours,tag] = line
            for m in month.split(','):
                for h in hours.split(','):
                    key = '_'.join([prov,m,h])
                    if key not in data :
                        data[key] = tag
                    if '.' not in hours:
                        key = '_'.join([prov, m, h + '.5'])
                        data[key] = tag

    return data




def tag_price(province,time):
    price_tags = load_info()
    month = time.split('-')[1]
    month = str(int(month))
    [h,m,s] = time.split()[1].split(':')
    h = int(h)
    m = int(m)
    if m >= 30:
        h = h+0.5
    h = str(h)
    key=province + '_' + month + '_' + h
    if key in price_tags:
        return price_tags[key]

    key =province + '_all_' + h
    if key in price_tags:
        return price_tags[key]
    else:
        return '2'


def get_name(time,province):
    #time = '2022-06-01 1:15:20'
    #province = '北京'
    tag = tag_price(province,time)
    name= {'4':'尖峰','3':'峰','2':'平','1':'谷'}
    #print(name[tag])
    return name[tag]
def str2arr(s):
    if type(s) is list :
        return s 
    s =  s[1:-1].replace("'","").split(',')
    return s 

if __name__ == '__main__':
    time = '2022-06-01 1:15:20'
    province = '北京'
    get_name(time,province)
