# coding:utf-8
"""抓取智联地区相关任务"""
import time
from logs import log
from page_parse.zlptdata import crawl_detail
from tasks.workers import app
from celery import Celery
from db.redis_db import Url_Sto
from db.mysql_db import insert_zhilian_data
import json


@app.task(ignore_result=True)
def excute_detail_task():
    keyword = Url_Sto.fetch_url_list('zhilian_list')
    """任务函数，抓取智联地区信息"""
    log.crawler.info('The crawler {} task is starting...'.format(keyword))
    item = crawl_detail(keyword)  # 此处可能有误
    if not item:
        with open('parse_fail_detail_url.txt', 'a', encoding='utf-8') as f:
            f.write(keyword + '\n')
        return
    # str_data = json.dumps(item, ensure_ascii=False)
    insert_zhilian_data(item)
    log.crawler.info('The crawler {} task has store mysql is ture'.format(keyword))
excute_detail_task()