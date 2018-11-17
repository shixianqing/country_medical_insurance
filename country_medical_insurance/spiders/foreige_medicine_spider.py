# -*- coding: utf-8 -*-
import scrapy
import chardet
import country_medical_insurance.util.fileUtil as util
import re
from scrapy.http.request import Request
from fake_useragent import UserAgent
from scrapy.selector import Selector
import time
from selenium import webdriver
import country_medical_insurance.dbtool as db
# from country_medical_insurance.items import ForeigeMedicineItem
ua = UserAgent()

"""
进口药品

"""
class ForeigeMedicineSpider(scrapy.Spider):
    name = 'foreige_medicine_spider'
    allowed_domains = ['http://app1.sfda.gov.cn/']
    url_pattern = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=36&bcId=152904858822343032639340277073&State=1&tableName=TABLE36&curstart={}'
    start_urls = []
    pool = db.MysqlPool()

    for i in range(1,286):start_urls.append(url_pattern.format(i))

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
              yield Request(url=u,dont_filter=True)
       elif(url.startswith("http://app1.sfda.gov.cn/datasearchcnda/face3/content.jsp")):
           textArr = []
           tdList = select.xpath("/html/body/div/div/table[1]/tbody/tr/td[2]")
           for k, td in enumerate(tdList):
               if k > 31:break
               textArr.append(td._root.text if td._root.text is not None else "")
           print("文本信息-------------》》》{}".format(textArr))
           sql = "INSERT INTO `scrapy_dev`.`foreign_medicine` (`registry_no`, `origin_registry_no`, `registry_no_remark`, `packge_allow_no`, `zh_comp_name`, `en_comp_name`, `zh_addr`, `en_addr`, `zh_area`, `en_area`, `zh_prod_name`, `en_prod_name`, `zh_trade_name`, `en_trade_name`, `zh_form`, `standard`, `packge_standard`, `zh_prod_comp`, `en_prod_comp`, `zh_prod_comp_addr`, `en_prod_comp_addr`, `zh_comp_country`, `en_comp_country`, `issue_cert`, `invalid_date`, `packge_comp_name`, `packge_comp_addr`, `packge_num_allow_date`, `package_num_invalid_date`, `prod_type`, `medicine_ben_code`, `medicine_ben_code_remark`) VALUES" \
                 "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
           self.pool.insert(sql,tuple(textArr))
           self.pool.end("commit")



