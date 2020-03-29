# -*- coding: utf-8 -*-
# @Time    : 2020/3/22 15:47
# @Author  : 结尾！！
# @FileName: spider_task_zbj.py
# @Software: PyCharm

import requests



#使用xpath
from scrapy.selector import Selector
header={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
def parse_zbj(html_url):
    resp=requests.get(html_url,headers=header)
    resp.encoding="utf-8"
    print("网页返回的状态码：",resp.status_code)
    code=resp.status_code
    if code==200:
        select=Selector(resp)
        demands=select.xpath('//*[@id="utopia_widget_7"]/div[@class="demand-list"]//div[@class="demand-card"]')
        print("总计有%d条发布信息."%len(demands))
        for div in demands:
            release_time=div.xpath('./div[@class="demand-card-head"]/span[1]/text()').extract_first().strip() #发布时间
            attend_num=div.xpath('./div[@class="demand-card-head"]/span[2]/text()').extract_first().strip() #参与人数
            title=div.xpath('./div[@class="demand-card-body"]/@title').extract_first().strip() #产品名称
            price=div.xpath('.//div[@class="demand-price"]/text()').extract_first().strip() #价格
            describe=div.xpath('.//div[@class="demand-card-desc"]/text()').extract_first().strip() #产品描述
            commodity=div.xpath('.//div[@class="demand-foot-tags flt"]/span/text()').extract_first() #招标方
            link=div.xpath('.//a[@class="prevent-defalut-link"]/@href').extract_first() #需求的连接
            print([release_time,attend_num,title,price,describe,commodity,link])
            line=[release_time, attend_num, title, price, describe, commodity, link]
            save_csv(line)
    else:
        print("爬虫被封了",html_url)
        return

import csv
import time
from datetime import datetime
now = datetime.now()
print(now)
def save_csv(lise_line):
    file = csv.writer(open("./2020-3-22-20-15.csv",'a',newline="",encoding="utf-8"))
    file.writerow(lise_line)

if __name__ == '__main__':
    url = "https://task.zbj.com/?s=2&so=2&ss=0"  # 为托管的连接
    for i in range(1,120):
        url_2 =f"https://task.zbj.com/page{i}.html?s=2&so=2&ss=0"  # 第二页的连接
        parse_zbj(url_2)
        time.sleep(2.5)

