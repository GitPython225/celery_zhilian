# coding: UTF - 8
import pymysql
import json
#
# cursor = conn.cursor()
#
# sql_insert = "insert into num (key_id, value_id) VALUES(%s,%s)"
# batch_data_list = []
# for i in range(10000000):
#     i = str(i)
#
#     batch_data_list.append((i,i))
# print(batch_data_list)
#     # break
# try:
#     cursor.executemany(sql_insert, batch_data_list)
#     print(cursor.rowcount)
#     conn.commit()
# except Exception as e:
#     print(sql_insert)
#     print(e)
# conn.rollback()
# cursor.close()
# conn.close()
