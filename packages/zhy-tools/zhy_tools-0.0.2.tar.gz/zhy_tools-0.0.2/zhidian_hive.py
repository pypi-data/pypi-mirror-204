#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Hongyu Zhao
@contact:zhaohongyu2401@yeah.com
@version: 1.0.0
@file: data2cloudHive.py
@time: 2022/8/30 09:33
"""

# #引入模块
from obs import ObsClient
# 创建ObsClient实例



obsClient = ObsClient(
    access_key_id='SCWIFW2DSFAXUI4V3N5P',
    secret_access_key='4LYu6ZCjmM8lTDz7hBVHOt2mEKBNf3gG4LIuNaEu',
    server='obs.cn-north-4.myhuaweicloud.com'
)


# 使用访问OBS
def putfile(bucketName, objectKey, file_path, flag='upload'):
    # 调用putContent接口上传对象到桶内
    # resp = obsClient.listObjects('obs-dli-upload')
    # resp = obsClient.putContent('obs-dli-upload', 'mqh_20220228', 'tmp_shence_miaosha_data_sql.sql')

    if flag == 'upload':
        # resp = obsClient.putFile('obs-dli-upload','mqh/test.csv','/Users/maqihao/Desktop/NewLink/算法/dli-sdk-python-1.0.8/examples/test.csv')
        resp = obsClient.putFile(bucketName, objectKey, file_path)
    elif flag == 'download':
        resp = obsClient.downloadFile(bucketName, objectKey, file_path)
        # resp = obsClient.downloadFile('obs-dli-upload', 'mqh_20220228/20210908.csv',downloadFile='obs://obs-dli-upload/mqh_20220228/20210908.csv')

    # print(resp)
    if resp.status < 300:
        # 输出请求Id
        print('requestId:', resp.requestId)
    else:
        # 输出错误码
        print('errorCode:', resp.errorCode)
        # 输出错误信息
        print('errorMessage:', resp.errorMessage)

def hive_run():
    import datetime
    pt = datetime.datetime.now()
    pt = pt.strftime('%Y-%m-%d')
    putfile('zhidian-algo','userid_dram_aigo/pt={now}/user_change_level.csv'.format(now=pt),
        '/root/work_place/zhy/kuaidian/data/feature_data/online_process/user_intent/user_change_level.csv')


    print('fresh data ')
    from dli_contrast import read_sql
    fresh_sql = """
        MSCK REPAIR TABLE  `zhidian_algo`.`user_dram_aigo`;
    """
    #test = read_sql(fresh_sql,['info']) 


if __name__=='__main__':
    hive_run()
