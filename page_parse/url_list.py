from page_parse import base_page
from lxml import etree
import header
from db.redis_db import Url_Sto
from logs import log


def crawl_zhilian_list(url):
    headers = header.headers
    log.crawler.info('The crawler task is crawling {} listpage'.format(url))
    resp = base_page.basic_page(url)
    # print(resp)
    if not resp:
        with open('noresp_url.txt', 'a', encoding='utf-8') as f:
            f.write(url + '\n')
        return
    html = etree.HTML(resp.content.decode())
    next_page_url = html.xpath('//div[@class="pagesDown"]/ul/li[@class="pagesDown-pos"]/a/@href')
    detail_urls = html.xpath('//td[@class="zwmc"]/div/a/@href')
    # print(next_page_url)
    # print(detail_urls)
    if next_page_url:
        crawl_zhilian_list(next_page_url[0])
    # for detail_url in detail_urls:
    Url_Sto.store_url_list('zhilian_list', detail_urls)  # 列表
