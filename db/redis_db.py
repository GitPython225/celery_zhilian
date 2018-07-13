import redis
import time

r = redis.Redis(host='localhost', port=6379, password='xxx', db=0, decode_responses=True)
urls_con = r.pipeline(transaction=True)


class Url_Sto(object):
    @classmethod
    def store_url(cls, name, url):
        urls_con.sadd(name, url)
        urls_con.execute()

    @classmethod
    def fetch_url(cls, name):
        # i = 0
        # while r.scard(name) == 0:  # 为空
        #     # 等待 waiting_size 秒
        #     i += 1
        #     time.sleep(1)
        #     if i >= 100:
        #         break
        urls_con.spop(name)
        url = urls_con.execute()  # 可以批量操作
        print(url)
        return url[0]

    @classmethod
    def store_url_list(cls, name, url):
        for l in url:
            urls_con.sadd(name, l)
        urls_con.execute()

    @classmethod
    def fetch_url_list(cls, name):
        # i = 0
        # while url_list_con.scard(name) == 0:  # 为空
        #     # 等待 waiting_size 秒
        #     i += 1
        #     time.sleep(1)
        #     if i >= 100:
        #         break
        urls_con.spop(name)
        url = urls_con.execute()  # 可以批量操作
        return url[0]
