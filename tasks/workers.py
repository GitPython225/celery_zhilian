# coding:utf-8
"""celery worker相关配置"""
import os
from datetime import datetime
from celery import Celery, platforms
from kombu import Exchange, Queue
from datetime import timedelta

"""Kombu是一个为Python写的消息库，目标是为AMQ协议提供一个傻瓜式的高层接口，让Python中的消息传递变得尽可能简单，并且也提供一些常见消息传递问题的解决方案"""

# 加载config配置信息
# from config.conf import (
#   get_broker_and_backend
#   get_redis_master
# )

# root模式下启动celery， 默认不能root启动celery
platforms.C_FORCE_ROOT = True

# 获取到日志路径
worker_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)) + '/logs', 'celery.log')
beat_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)) + 'logs', 'beat.log')
# broker_and_backend = get_broker_and_backend()
# tasks = ['tasks.area', 'tasks.zhilist', 'tasks.zhidetail']
tasks = ['tasks.listpage']
# 'tasks.area',# 创建celery app实例
# if isinstance(broker_and_backend, list):
#     broker, backend = broker_and_backend
app = Celery('zhi_task', include=tasks, broker='redis://:Btxrrvt.1@localhost:6379/7',
             backend='redis://:Btxrrvt.1@localhost/8')

# CELERY_IMPORTS = ('tasks.listpage',)
app.conf.update(

    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERYBEAT_SCHEDULE={
        'list_task': {
            'task': 'tasks.listpage.excute_list_task',
            'schedule': 1,  # 抓取时间间隔
            'options': {'queue': 'crawler_list_queue', 'routing_key': 'list_info'}
        },
        #     'detail_task': {
        #         'task': 'tasks.zlpt.excute_detail_task',
        #         'schedule': 1,  # 抓取时间间隔
        #         'options': {'queue': 'crawler_detail_queue', 'routing_key': 'detail_info'}
        #     },
        # #     #     'area_task': {
        # #     #         'task': 'tasks.area.excute_area_task',
        # #     #         'schedule': timedelta(hours=1),
        # #     #         'options': {'queue': 'crawler_area_queue', 'routing_key': 'area_info'}
        # #     #     }
    },
    CELERY_QUEUES=(
        Queue('crawler_list_queue', exchange=Exchange('crawler_list_queue', type='direct'), routing_key='list_info'),
        #
        # Queue('crawler_detail_queue', exchange=Exchange('crawler_detail_queue', type='direct'),
        #       routing_key='detail_info'),
        # Queue('crawler_area_queue', exchange=Exchange('crawler_area_queue', type='direct'), routing_key='area_info'),
        # Queue('crawler_town_queue', exchange=Exchange('crawler_town_queue', type='direct'), routing_key='road_info'),
        # 此处可能有错误
    ),

)
