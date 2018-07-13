from lxml import etree
from page_parse.base_page import basic_page
import json
from datetime import datetime
from db import mysql_db
from db.redis_db import Url_Sto
import time
from logs import log


def crawl_detail(url):
    log.crawler.info('The crawler task is crawling {} detailpage '.format(url))
    resp = basic_page(url)
    print(resp)
    if not resp:
        with open('fail_detail_url.txt', 'a', encoding='utf-8') as f:
            f.write(url + '\n')
        return
    response = etree.HTML(resp.content.decode())
    if "xiaoyuan" in url:
        job_name = response.xpath('//*[@id="JobName"]/text()')[0]
        com_name = response.xpath('//*[@id="jobCompany"]/a/text()')[0]
        com_res_rate = None
        com_tm = None  # 公司待遇
        job_mon_pay = None
        job_workplace = response.xpath('//*[@id="currentJobCity"]/text()')[0]
        job_pub = response.xpath('//*[@id="liJobPublishDate"]/text()')[0]
        job_natu = None
        # 工作经验
        job_expe = None
        # 最低学历
        min_degree = None
        # print(type(min_degree))
        # 招聘人数
        rec_number = response.xpath('//*[@id="divMain"]/div/div/div[1]/div[1]/ul[2]/li[6]/text()')[0]
        # 职位类别
        job_cate = response.xpath('//*[@id="divMain"]/div/div/div[1]/div[1]/ul[2]/li[4]/text()')[0]
        # 工作职责
        com_resp = response.xpath(
            '//*[@id="divMain"]/div/div/div[1]/div[2]/div[2]/div/p/text()')
        com_intr = response.xpath(
            '//*[@id="divMain"]/div/div/div[1]/div[2]/div[2]/div//text()')
        com_sca = response.xpath(
            '//*[@id="divMain"]/div/div/div[1]/div[1]/ul[1]/li[6]/text()')[0]
        # 公司性质
        com_natu = response.xpath(
            '//*[@id="divMain"]/div/div/div[1]/div[1]/ul[1]/li[8]/text()')[0]
        # 公司行业
        com_indu = \
            response.xpath('//*[@id="divMain"]/div/div/div[1]/div[1]/ul[1]/li[4]/text()')[0]
        com_hpage_url = 'https://xiaoyuan.zhaopin.com' + response.xpath(
            '//*[@id="divMain"]/div/div/div[2]/div[1]/div/div/a[1]/@herf')[0]
        com_addr = response.xpath('//*[@id="divMain"]/div/div/div[2]/div[2]/div/p/text()')[0]
        item = {}
        item['job_name'] = job_name
        item['source'] = 'zhilian'
        item['company_name'] = com_name
        item['com_res_rate'] = com_res_rate
        item['company_pay'] = com_tm
        item['monthly_pay'] = job_mon_pay
        item['workplace'] = job_workplace
        item['published_data'] = job_pub
        item['job_nature'] = job_natu
        item['experience'] = job_expe
        item['minimum_education'] = min_degree
        item['recruitment'] = rec_number
        item['job_category'] = job_cate
        item['operating_duty'] = com_resp
        item['job_requirement'] = 'None'
        item['company_introduction'] = com_intr
        item['company_size'] = com_sca
        item['company_nature'] = com_natu
        item['company_industry'] = com_indu
        item['company_domain'] = com_hpage_url
        item['company_adress'] = com_addr
        # item['collect_data'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        # .strftime('%Y-%m-%d %H:%M:%S')

        item['job_url'] = url
        item['KeyNo'] = 'zhilian'
        return item
    else:
        code = url.split('.')[-2].split('/')[-1]
        code = code[:-6] + 'J90' + code[-6:]
        c_url = 'http://jobs.zhaopin.com/ResumeFeedback.ashx?positionNumber=CC%s000' % code
        resp_data = basic_page(c_url)
        if not resp_data:
            with open('fail_detail_url.txt', 'a', encoding='utf-8') as f:
                f.write(c_url + '\n')
            return
        data = json.loads(resp_data.content.decode())
        job_name = response.xpath('//h1/text()')
        try:
            try:
                job_name = response.xpath('//h1/text()')[0]
                # 企业名称
            except Exception:
                pass
            else:
                job_name = job_name
                com_name = response.xpath('//h5/a[1]/text()')
                if com_name:
                    com_name = com_name[0]
                else:
                    com_name = response.xpath('/html/body/div[5]/div[1]/div[1]/h2/a/text()')[0]
                # 企业答复率
                # print response.body
                com_res_rate = data[u'Probability'] + '%'
                if com_res_rate == '%':
                    com_res_rate = 'None'
                # 公司待遇
                com_tm = response.xpath('//div[@class="welfare-tab-box"]//text()')
                com_tm = ''.join(com_tm)
                # 职位月薪
                job_mon_pay = response.xpath('//ul/li/strong/text()')[0]
                # 工作地点
                job_workplace = response.xpath('//ul[@class="terminal-ul clearfix"]/li[2]/strong//text()')
                job_workplace = ''.join(job_workplace)
                # 发布日期
                job_pub = response.xpath('//ul/li/strong/span/text()')[0]

                # job_pub = time.strptime(job_pub, "%Y-%m-%d %H:%M:%S")
                # job_pub = time.strftime("%Y-%m-%d %H:%M:%S",job_pub)

                job_natu = response.xpath('//ul[@class="terminal-ul clearfix"]/li[4]/strong/text()')[0]
                # 工作经验
                job_expe = response.xpath('//ul[@class="terminal-ul clearfix"]/li[5]/strong/text()')[0]
                # 最低学历
                min_degree = response.xpath('//ul[@class="terminal-ul clearfix"]/li[6]/strong/text()')[0]
                # print(type(min_degree))
                # 招聘人数
                rec_number = response.xpath('//ul[@class="terminal-ul clearfix"]/li[7]/strong/text()')[0]

                # 工作性质
                # print job_pub
                # job_natu = response.xpath('//ul/li/strong/text()').extract()[2]
                # # 工作经验
                # job_expe = response.xpath('//ul/li/strong/text()').extract()[3]
                # # 最低学历
                # min_degree = response.xpath('//ul/li/strong/text()').extract()[4]
                # # 招聘人数
                # rec_number = response.xpath('//ul/li/strong/text()').extract()[5].split(u'人')[0]
                # 职位类别
                job_cate = response.xpath('//ul[@class="terminal-ul clearfix"]/li/strong/a/text()')[-1]
                # 工作职责
                com_resp = response.xpath(
                    '//div[@class="tab-cont-box"][1]/div[@class="tab-inner-cont"][1]//text()')
                com_resp = ''.join(com_resp).replace(' ', '').replace('\t', '').replace('\n', '').replace(u'全选',
                                                                                                          '').replace(
                    u'查看更多相似职位推荐>>', '').replace('\r', '')
                # 岗位要求/任职资格
                # job_desc = response.xpath('').extract_first()
                # 公司介绍
                com_intr = response.xpath(
                    '//div[@class="tab-cont-box"][1]/div[@class="tab-inner-cont"][2]//text()')
                com_intr = ''.join(com_intr).replace(' ', '').replace('\t', '').replace('\n', '').replace(u'全选',
                                                                                                          '').replace(
                    u'查看更多相似职位推荐>>', '').replace('\r', '')
                # 公司规模
                com_sca = response.xpath(
                    '//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[1]/strong/text()')[0]
                # 公司性质
                com_natu = response.xpath(
                    '//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[2]/strong/text()')[0]
                # 公司行业
                com_indu = \
                    response.xpath('//ul[@class="terminal-ul clearfix terminal-company mt20"]/li/strong/a/text()')[0]
                # 公司主页
                try:
                    com_hpage_url = response.xpath(
                        '//ul[@class="terminal-ul clearfix terminal-company mt20"]/li/strong/a/text()')[1]
                    if 'http' in com_hpage_url:
                        com_hpage_url = com_hpage_url
                    else:
                        com_hpage_url = None
                except Exception:
                    com_hpage_url = None
                # 公司地址

                com_addr = response.xpath(
                    '//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[5]/strong/text()')
                if com_addr:
                    com_addr = com_addr[0].strip()
                else:
                    com_addr = response.xpath('//div[@class="tab-inner-cont"]/h2/text()')[0].strip()
        except:
            print(url)
        else:
            item = {}
            item['job_name'] = job_name
            item['source'] = 'zhilian'
            item['company_name'] = com_name
            item['com_res_rate'] = com_res_rate
            item['company_pay'] = com_tm
            item['monthly_pay'] = job_mon_pay
            item['workplace'] = job_workplace
            item['published_data'] = job_pub
            item['job_nature'] = job_natu
            item['experience'] = job_expe
            item['minimum_education'] = min_degree
            item['recruitment'] = rec_number
            item['job_category'] = job_cate
            item['operating_duty'] = com_resp
            item['job_requirement'] = 'None'
            item['company_introduction'] = com_intr
            item['company_size'] = com_sca
            item['company_nature'] = com_natu
            item['company_industry'] = com_indu
            item['company_domain'] = com_hpage_url
            item['company_adress'] = com_addr
            # item['collect_data'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            # .strftime('%Y-%m-%d %H:%M:%S')

            item['job_url'] = url
            item['KeyNo'] = 'zhilian'
            return item
