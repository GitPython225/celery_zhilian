# redis的管道技术用于提高对redis的操作效率
import redis, time, pymysql
from util.redis_bloom import bloom_url

r1 = redis.Redis(host="localhost", password='Btxrrvt.1', port=6379, db='0', decode_responses=True)
pipe1 = r1.pipeline(transaction=True)
conn = pymysql.Connect(host='localhost', port=3306, user='root', passwd='Btxrrvt.1', db='zhilian',
                       charset='utf8')
cursor = conn.cursor()

if pipe1.scard('zhilian_list') > 10000:
    for i in range(10000):
        pipe1.spop('zhilian_list')

insert_sql = 'insert into zl(href) VALUES (%s)'
try:
    cursor.executemany(insert_sql, pipe1.execute())
    print(cursor.rowcount)
    conn.commit()
except Exception as e:
    print(e)
conn.rollback()

conn.close()
cursor.close()

# r2 = redis.Redis(host="", password='Btxrrvt.1', port=6379, db='2', decode_responses=True)
# pipe2 = r2.pipeline(transaction=True)
# for i in range(3344):
#     pipe2.srandmember('智联')
# print(pipe1.execute())

# for i in range(100):
#     pipe1.sadd('智联', i)
# pipe1.execute()
# for i in range(100):
#     pipe1.spop('智联')
# print(pipe1.execute())
# print(pipe.spop('pipe'))
# time1 = time.time()
# for key in range(1000):
# pipe2.sadd('智联',
#            " http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E8%BE%BD%E5%AE%81&isjts=1&isfilter=1&p=1&fjt=10004")  # 10w 4  100w 35
# pipe2.execute()
# print(time.time()-time1)
# for key in range(10000):
#     r.set('redis', str(key))  # 10w 16 100w 176
# from datetime import datetime
# create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# print(type(datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')))
# print(create_time)
# print(type(create_time))
