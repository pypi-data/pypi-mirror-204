#!/usr/bin/python
# -*- coding: UTF-8 -*-

from dli.dli_client import DliClient
from dli.download_job import DownloadJob
from dli.logger import logger
import pandas as pd

import time

region = "cn-north-4"
endpoint = "dli.cn-north-4.myhuaweicloud.com"
obs_endpoint = ""
project_id = "0dfc32615b00f3802f12c00408441dc6"
username = ""
ak = "N5VJSZR9AIQXHBFJTLLU"
sk = "4iRGqUc8mGYGnHuYehbtVpBsMLvbtsIlQ91F18ZM"
queue_name = "schedule_normal_sql"

#电
endpoint = "dli.cn-north-4.myhuaweicloud.com"
project_id = "0e837d51b400f3452fadc002163f58d5"
ak = "SCWIFW2DSFAXUI4V3N5P"
sk = "4LYu6ZCjmM8lTDz7hBVHOt2mEKBNf3gG4LIuNaEu"



def print_res(download_job):
    status = download_job.get_download_status()
    while status not in ('FINISHED', 'CANCELLED'):
        status = download_job.get_download_status()
        time.sleep(1)
    obs_reader = download_job.create_reader()
    s=[]
    count = 0
    for record in obs_reader:
        count += 1
        s.append(record)
    return s
        # print(record)
    logger.info("total records: %d" % count)


def read_sql(sql,target_columns=None):
    kwargs = {
        'region': region,
        'project_id': project_id,
        'auth_mode': 'aksk',
        'ak': ak,
        'sk': sk,
        'endpoint': endpoint,
    }
    dli_client = DliClient(**kwargs)
    sql_conf = {'spark.sql.enableToString': 'false' , 'spark.sql.adaptive.join.enabled': 'true', 'spark.sql.adaptive.enabled':'true',
        'spark.sql.adaptive.skewedJoin.enabled':'true','spark.sql.adaptive.enableToString':'false','spark.sql.adaptive.skewedPartitionMaxSplits':'10'}    

    # logger.info("download specify table data")
    # print_result(DownloadJob(dli_client, queue_name, "tpch", "nation"))
    a = time.time()
    logger.info("download query result")
    sql_job = dli_client.execute_sql(sql, queue_name=queue_name,options=sql_conf)
    if target_columns == None : return 0 
    df_copy = print_res(DownloadJob(dli_client, queue_name, "", "", job=sql_job))
    df_copys = [eval(str(x)) for x in df_copy]
    if target_columns :
        df_features = pd.DataFrame(df_copys, columns=target_columns)
    else:
        df_features = pd.DataFrame(df_copys)
    b = time.time()
    print("时间：{}".format((b-a)/60))
    return df_features
if __name__ == '__main__':
    target_columns = ['user_id', 'expire_date_start']
