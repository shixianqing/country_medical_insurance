# -*- coding: utf-8 -*-
from country_medical_insurance.util.redisUtil import Jedis
from scrapy.http.request import Request
from fake_useragent import UserAgent
from scrapy.selector import Selector
from country_medical_insurance.items import CountryMedicalInsuranceItem
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
import country_medical_insurance.util.fileUtil as fileUtil
ua = UserAgent()

class MedicineSpider(RedisSpider):
    name = 'medicine_spider'
    allowed_domains = ['http://app1.sfda.gov.cn/']
    url_pattern = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=25&State=1&bcId=152904713761213296322795806604&curstart={}'
    # start_urls = []
    redis_key = 'medicineSpider:start_urls'
    uls = fileUtil.read_time_out_url()
    for line in uls:Jedis().client.lpush(redis_key,line.replace("\n", ""))
    for i in range(1,11111):Jedis().client.lpush(redis_key,url_pattern.format(i))#11111

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.set_page_load_timeout(30)

    def parse(self, response):

       html = response.body.decode("utf-8")
       select = Selector(text=html)
       url = response.url
       if url.startswith("http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp"):
           a_el_list = select.xpath("/html/body/table[2]/tbody/tr/td/p/a/@href").extract()
           for a_el in a_el_list:
              u = "http://app1.sfda.gov.cn/datasearchcnda/face3/"+a_el.split(",")[1].replace("'", "")
              self.log("detail_url------------->>>{}".format(u))
              yield Request(url=u,callback=self.parse_item,dont_filter=True)
       else:
           self.parse_item(response)


    def parse_item(self, response):
        select = Selector(text=response.body.decode("utf-8"))
        texts = select.css("div>div>table:nth-child(1)>tbody>tr>td:nth-child(2)")
        textArr = []
        for k, p in enumerate(texts):
            if k > 12: break
            text = p._root.text
            textArr.append(text if text is not None else "")

        item = CountryMedicalInsuranceItem()
        item["info"] = textArr
        yield item




