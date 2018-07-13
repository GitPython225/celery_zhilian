# coding: UTF - 8
import pymysql
from datetime import datetime
import json


def insert_zhilian_data(item):
    batch_data_list = []
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = ('智联',
            item["job_name"], item["company_name"], item["com_res_rate"], item["company_pay"], item["monthly_pay"],
            item["workplace"], item["published_data"], item["job_nature"], item["experience"],
            item["minimum_education"],
            item["recruitment"], item["job_category"], item["operating_duty"], item["job_requirement"],
            item["company_introduction"], item["company_size"], item["company_nature"], item["company_industry"],
            item["company_domain"], item["company_adress"], item["job_url"], item['KeyNo'], create_time)
    batch_data_list.append(data)
    conn = pymysql.Connect(host='localhost', port=3306, user='root', passwd='python', db='zhilian',
                           charset='utf8')

    cursor = conn.cursor()
    insert_sql = "insert into company_recruit_information(source, job_name,company_name,com_res_rate,company_pay,monthly_pay,workplace,published_data,job_nature,experience,minimum_education,recruitment,job_category,operating_duty,job_requirement,company_introduction,company_size,company_nature,company_industry,company_domain,company_adress,job_url,keyno,collect_data) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s)"
    try:
        cursor.executemany(insert_sql, batch_data_list)
        print(cursor.rowcount)
        conn.commit()
    except Exception as e:
        print(e)
    conn.rollback()
    cursor.close()
    conn.close()
