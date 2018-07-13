# coding: UTF - 8
import pymysql
# from config.conf import batch_data_list
from db.redis_db import Data_Get
from datetime import datetime
import json

batch_data_list = []
# i = 0
while True:
    try:
        item = json.loads(Data_Get.fetch_url_list('item'))
    except Exception as e:
        print(e)
    else:
        item['collect_data'] = datetime.today()

        batch_data_list.append((
                item["job_name"], '智联',item["company_name"], item["com_res_rate"], item["company_pay"], item["monthly_pay"],
                item["workplace"], item["published_data"], item["job_nature"], item["experience"], item["minimum_education"],
                item["recruitment"], item["job_category"], item["operating_duty"], item["job_requirement"],
                item["company_introduction"], item["company_size"], item["company_nature"], item["company_industry"],
                item["company_domain"], item["company_adress"], item["collect_data"], item["job_url"], item['KeyNo']))
        if len(batch_data_list) == 1000:
            conn = pymysql.Connect(host='localhost', port=3306, user='root', passwd='python', db='zhilian', charset='utf8')
            cursor = conn.cursor()
            sql_insert = "insert into company_recruit_information(job_name,source,company_name,com_res_rate,company_pay,monthly_pay,workplace,published_data,job_nature,experience,minimum_education,recruitment,job_category,operating_duty,job_requirement,company_introduction,company_size,company_nature,company_industry,company_domain,company_adress,collect_data,job_url,keyno) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s)"
            try:
                cursor.executemany(sql_insert, batch_data_list)
                print(cursor.rowcount)
                conn.commit()
            except Exception as e:
                print(e)
            conn.rollback()
            cursor.close()
            conn.close()
            batch_data_list = []
