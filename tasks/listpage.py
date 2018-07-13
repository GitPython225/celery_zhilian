# coding:utf-8
"""抓取智联地区相关任务"""
import time
from logs import log
from page_parse.url_list import crawl_zhilian_list
from tasks.workers import app
from celery import Celery
from db.redis_db import Url_Sto
from urllib.parse import unquote_plus  # 第一次运行出错，用于处理错误


# @app.task(ignore_result=True)
def excute_list_task():
    keyword = Url_Sto.fetch_url('智联')
    """任务函数，抓取智联地区信息"""
    print(keyword)
    if not keyword:
        return
    crawl_zhilian_list(keyword)  # 此处可能有误
    log.crawler.info('The crawler {} task is starting...'.format(keyword))
for i in range(50):
    excute_list_task()
