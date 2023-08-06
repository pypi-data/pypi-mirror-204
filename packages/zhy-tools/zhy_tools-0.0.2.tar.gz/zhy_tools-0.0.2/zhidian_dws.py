import psycopg2
import pandas as pd 
def read_sql(sql,header=None):
    
    conn = psycopg2.connect(database='newlink',user='bigdata_algorithm_r',password='eCE#2t*uz!DqbPsY',host='10.65.5.206',port=8000)
    cur = conn.cursor()
    if not header :
        cur.execute(sql)
    else:
        cur.execute(sql)
        rows = cur.fetchall()
        datas = []
        for row in rows :
            datas.append(list(row))
        df = pd.DataFrame(datas,columns=header)
        return df 
    return 0 

if __name__ == '__main__':
    sql =  """
    SELECT 
    f_charge_station_code,
    hour(f_start_charge_time) as time_num,
    count(*)
    FROM fp_order.t_charge_order_info 
    where f_start_charge_time >= '2023-03-20 00:00:00' and f_start_charge_time < '2023-03-21 00:00:00'
    and f_original_total_money > 1 and f_equipment_type = 4 
	and f_order_source = 10088001
    group by 1,2
    limit 11
    """
    df = read_sql(sql,['sid','hour','orders'])
    print(df)