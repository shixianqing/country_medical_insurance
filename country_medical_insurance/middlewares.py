# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
import time
from country_medical_insurance.util.redisUtil import Jedis
from scrapy.selector import Selector
from country_medical_insurance.util.logger import Log

logegr = Log("CustomDownloaderMiddleware")


class CustomDownloaderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        s.exception_path = crawler.settings.get("FAIL_LOG_PATH")
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        url = request.url
        try:
            spider.browser.get(url)
        except TimeoutException as e:
            logegr.error(msg="{} --- 超时 ---- {}".format(url, e))
            Jedis().lpush(key="error_url", val=url)
            return request
        time.sleep(2)
        html = spider.browser.page_source
        selector = Selector(text=html)
        title = selector.xpath('/html/body/div/div/table[1]/tbody/tr[1]/td/div[1]/text()').extract_first()
        pageNo = selector.xpath('/html/body/table[4]/tbody/tr/td[1]/text()').extract_first()
        if not title and not pageNo:
            logegr.error("{}--------页面没有渲染成功".format(url))
            Jedis().lpush(key="error_url", val=url)
            return request
        # spider.browser.close()
        return HtmlResponse(url=url, body=html, encoding="utf-8",
                            request=request)

    def process_response(self, request, response, spider):
        if response.status != 200:
            Jedis().lpush(key="error_url", val=response.url)
            return request
        return response

    def process_exception(self, request, exception, spider):
        logegr.error("{}出现异常".format(request.url))
        Jedis().lpush(key="error_url", val=request.url)
        return request

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
