from header import headers
import requests
from util.get_proxy import func_proxy
# from util.bloom_filter import bloom_url
from util.redis_bloom import bloom_url
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def basic(url):
    resp = requests.get(url, headers=headers, proxies=func_proxy(), verify=False)
    print(url)
    print(resp)
    return resp


def basic_page(url, flag=False):
    if flag:
        return basic(url)
    else:
        if bloom_url(url):
            i = 1
            while i:
                try:
                    resp = basic(url)
                except Exception as e:
                    print(e)
                    i += 1
                    if i >= 10:
                        with open('timeout_url.txt', 'a', encoding='utf-8') as f:
                            f.write(url + '\n')
                        return
                    else:
                        continue
                else:
                    return resp
