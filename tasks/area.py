# coding:utf-8
"""抓取智联地区相关任务"""
import time
from logs import log
from page_parse.area import excute_city_url, excute_town_url, excute_road_url
from page_parse.url_list import crawl_zhilian_list
from tasks.workers import app
from celery import Celery
from db.redis_db import Url_Sto


@app.task(ignore_result=True)
def excute_road_task(url_list):
    for url in url_list:
        road_url_list = excute_road_url(url)
        if not road_url_list:
            continue
        log.crawler.info('The Three crawler {} task is starting...'.format(url))
        if isinstance(road_url_list, list):
            print(road_url_list)
            for road_url in road_url_list:
                Url_Sto.store_url('智联', road_url)
        else:
            Url_Sto.store_url('智联', road_url_list)


@app.task(ignore_result=True)
def excute_town_task(url_list):
    print('你好')
    for url in url_list:
        town_url_list = excute_town_url(url)
        # print(town_url_list)
        if not town_url_list:
            continue
        log.crawler.info('The two crawler {} task is started..'.format(url))
        if isinstance(town_url_list, list):
            # app.send_task('tasks.area.excute_road_task', args=(town_url_list,), queue='crawler_town_queue',
            #           routing_key='road_info')
            excute_road_task(town_url_list)
        else:
            Url_Sto.store_url('智联', town_url_list)


@app.task(ignore_result=True)
def excute_area_task():
    print("执行celery")
    """任务函数，抓取智联地区信息"""
    city_url_list = excute_city_url("http://jobs.zhaopin.com/citymapsj006.html")
    print(city_url_list)
    if not city_url_list:
        return
    # 此处可能有误
    log.crawler.info('The crawler area_url task is started..')
    # app.send_task('tasks.area.excute_town_task', args=(city_url_list,), queue='crawler_area_queue',
    #               routing_key='area_info')
    excute_town_task(city_url_list)

excute_area_task()
