# -*- coding: utf-8 -*-
from country_medical_insurance.util.redisUtil import Jedis
from scrapy.http.request import Request
from scrapy.selector import Selector
from country_medical_insurance.items import CountryMedicalInsuranceItem
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from country_medical_insurance.items import ForeigeMedicialItem
import re


class MedicineSpider(RedisSpider):
    name = 'medicine_spider'
    allowed_domains = ['http://app1.sfda.gov.cn/']
    url_pattern = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=25&State=1&bcId=152904713761213296322795806604&curstart={}'
    # start_urls = []
    redis_key = 'medicineSpider:start_urls'
    start_url = "http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=25&bcId=152904713761213296322795806604"

    # uls = fileUtil.read_time_out_url()
    # for line in uls:Jedis().client.lpush(redis_key,line.replace("\n", ""))
    # for i in range(1,2):Jedis().client.lpush(redis_key,url_pattern.format(i))#11111

    def __init__(self):
        self.browser = webdriver.Chrome()
        # self.browser.set_page_load_timeout(30)

    def parse(self, response):

        select = Selector(text=response.text)
        url = response.url
        if url == self.start_url:
            click_url = select.xpath("/html/body/table[4]/tbody/tr/td[6]/img/@onclick").extract_first()
            totalPage = int("".join(re.findall("[0-9]", click_url)))
            for i in range(1, 1 + 1):
                # yield Request(url=self.url_pattern.format(i), callback=self.parse, dont_filter=True)
                Jedis().lpush(key=self.redis_key, val=self.url_pattern.format(i))

        else:
            a_el_list = select.xpath("/html/body/table[2]/tbody/tr/td/p/a/@href").extract()
            for a_el in a_el_list:
                u = "http://app1.sfda.gov.cn/datasearchcnda/face3/" + a_el.split(",")[1].replace("'", "")
                self.log("detail_url------------->>>{}".format(u))
                yield Request(url=u, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        select = Selector(text=response.text)
        texts = select.css("div>div>table:nth-child(1)>tbody>tr>td:nth-child(2)")
        textArr = []
        for k, p in enumerate(texts):
            if k > 12: break
            aText = p.xpath("./a/text()").extract_first()
            if aText is not None:
                textArr.append(aText if aText else "")
                continue
            text = p._root.text
            textArr.append(text if text else "")

        item = CountryMedicalInsuranceItem()
        item["info"] = textArr
        item["url"] = response.url
        yield item

    def start_requests(self):
        yield Request(url=self.start_url, callback=self.parse, dont_filter=True)


"""
进口药品

"""


class ForeigeMedicineSpider(RedisSpider):
    name = 'foreige_medicine_spider'
    allowed_domains = ['http://app1.sfda.gov.cn/']
    url_pattern = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=36&bcId=152904858822343032639340277073&State=1&tableName=TABLE36&curstart={}'
    redis_key = 'foreige_medicine_spider:start_urls'
    start_url = "http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=36&bcId=152904858822343032639340277073"

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.set_page_load_timeout(30)

    def parse(self, response):

        select = Selector(text=response.text)
        url = response.url
        if url == self.start_url:
            click_url = select.xpath("/html/body/table[4]/tbody/tr/td[6]/img/@onclick").extract_first()
            totalPage = int("".join(re.findall("[0-9]", click_url)))
            for i in range(1, totalPage + 1):
                # yield Request(url=self.url_pattern.format(i), callback=self.parse, dont_filter=True)
                Jedis().lpush(key=self.redis_key, val=self.url_pattern.format(i))
        else:
            a_el_list = select.xpath("/html/body/table[2]/tbody/tr/td/p/a/@href").extract()
            for a_el in a_el_list:
                u = "http://app1.sfda.gov.cn/datasearchcnda/face3/" + a_el.split(",")[1].replace("'", "")
                self.log("detail_url------------->>>{}".format(u))
                yield Request(url=u, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        select = Selector(response=response)
        textArr = []
        tdList = select.xpath("/html/body/div/div/table[1]/tbody/tr/td[2]")
        for k, td in enumerate(tdList):
            if k > 31: break
            textArr.append(td._root.text if td._root.text else "")
        item = ForeigeMedicialItem()
        item["info"] = textArr
        item["url"] = response.url
        yield item

    def start_requests(self):

        yield Request(url=self.start_url, callback=self.parse, dont_filter=True)
