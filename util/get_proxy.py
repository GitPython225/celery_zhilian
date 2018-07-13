import json, random
import pymysql


def func_proxy():
    db = pymysql.connect(host='xxx', port=3306, user="xxx", passwd="xxx", db="zhilian",
                         charset='utf8')

    cursor = db.cursor()

    # SQL 更新语句
    sql = "select ip from ip_porxy"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        results = cursor.fetchall()

    except:
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    db.close()
    # print random.choice(results)[0]
    proxy = {}
    proxy['http'] = "http://" + random.choice(results)[0]
    # print(proxy)
    return proxy

print(func_proxy())
