import requests
import time
import header
import random
from lxml import etree
from page_parse.base_page import basic_page
from db.redis_db import Url_Sto
from urllib.parse import quote_plus
from db.redis_db import Url_Sto


# from page_parse.url_list import crawl_zhilian_list

def crawl_zlhome_list(html):
    # headers = header.headers
    # log.crawler.info('The crawler task is crawling {} listpage'.format(url))
    # resp = base_page.basic_page(url)
    # if not resp:
    #     with open('noresp_url.txt', 'a', encoding='utf-8') as f:
    #         f.write(url + '\n')
    #     return
    # html = etree.HTML(resp.content.decode())
    next_page_url = html.xpath('//div[@class="pagesDown"]/ul/li[@class="pagesDown-pos"]/a/@href')
    detail_urls = html.xpath('//td[@class="zwmc"]/div/a/@href')
    # print(next_page_url)
    # print(detail_urls)
    Url_Sto.store_url_list('zhilian_list', detail_urls)  # 列表
    if next_page_url:
        return next_page_url[0]


def excute_city_url(url):
    """抓取省会城市url"""
    resp = basic_page(url, True)
    if not resp:
        with open('noresp_url.txt', 'a', encoding='utf-8') as f:
            f.write(url + '\n')
        return
    resp = resp.content.decode()
    html = etree.HTML(resp)
    citise = html.xpath('//dd/a/text()')
    city_list = []
    for city in citise:
        url_city = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%s' % quote_plus(city)
        # print(url_city)
        city_list.append(url_city)
    return city_list


def excute_town_url(url):
    resp = basic_page(url)
    if not resp:
        with open('noresp_url.txt', 'a', encoding='utf-8') as f:
            f.write(url + '\n')
        return
    resp = resp.content.decode()
    html = etree.HTML(resp)
    total_number = html.xpath('//span/em/text()')[0]
    print(str(total_number) + url)
    town_url_list = []
    if int(total_number) > 5000:
        town = html.xpath(
            '//div[@class="newlist_list1 "]/div[@class="clearfix"]/div[@class="search_newlist_topmain1 fl"]/a/@href')
        """/html/body/div[3]/div[3]/div[1]/div[4]/div[1]/div[2]/a"""
        if town:
            for i in town[1:]:
                print('二级url')
                print(i)
                town_url = 'http://sou.zhaopin.com' + i

                town_url_list.append(town_url)
            return town_url_list
        else:
            town = html.xpath("/html/body/div[3]/div[3]/div[1]/div[5]/div/div[2]/a/@href")
            for i in town[1:]:
                print('二级url')
                print(i)
                town_url = 'http://sou.zhaopin.com' + i
                Url_Sto.store_url('智联', town_url)
    else:
        url2 = crawl_zlhome_list(html)
        return url2


def excute_road_url(url):
    road_url_list = []

    resp = basic_page(url)
    if not resp:
        with open('noresp_url.txt', 'a', encoding='utf-8') as f:
            f.write(url + '\n')
        return
    resp = resp.content.decode()
    html = etree.HTML(resp)
    total_number = html.xpath('//span/em/text()')
    if not total_number:
        with open('fail_url.txt', 'a', encoding='utf-8') as f:
            f.write(url)
    elif int(total_number[0]) > 6000:
        try:
            roads = html.xpath('//div[@class="search_newlist_mainwrap"][1]/a/text()')
            """/html/body/div[3]/div[3]/div[1]/div[4]/div[2]/a"""
            if roads:
                for road in roads[1:]:
                    url1 = url + '&ga=' + quote_plus(road)
                    print(url1)
                    road_url_list.append(url1)  # 此处可能作为字典的键
            return road_url_list
        except:
            print('错误的url为：', url)
    else:
        url2 = crawl_zlhome_list(html)
        # if not url2:
        #     with open('noresp_url.txt', 'a', encoding='utf-8') as f:
        #         f.write(url + '\n')
        #     return
        return url2
