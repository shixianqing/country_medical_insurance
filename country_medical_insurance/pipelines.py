# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import country_medical_insurance.dbtool as db
from country_medical_insurance.util.fileUtil import writeFile
from country_medical_insurance.util.fileUtil import writeDataIntoExcel
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from country_medical_insurance.items import ForeigeMedicialItem

setting = get_project_settings()


class CountryMedicalInsurancePipeline(object):

    # pool = db.MysqlPool()

    def process_item(self, item, spider):

        info = item["info"]
        if not info:
            writeFile(url=item["url"],fileName=setting.get("FAIL_LOG_PATH"))
            raise DropItem("未获取到国产器械信息，丢弃。{}".format(item["url"]))

        # if isinstance(item, ForeigeMedicialItem):
        #     self.process_foreige_medicine(item)
        # else:
        #     self.process_country_medicine(item)

        # sql = "insert into country_medicine(allow_no,medicine_name,en_name,trade_name,form,medicine_size,prod_unit,prod_addr," \
        #       "prod_type,allow_date,origin_allow_no,medicine_ben_code,code_remark) " \
        #       "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # print("sql---===========>>>" + sql)
        # try:
        #     self.pool.insert(sql, param=tuple(tuple(info)))
        #     self.pool.end("commit")
        # except BaseException as e:
        #     # print(e)
        #     print("数据插入失败！")
        #     writeFile(url=item["url"], fileName="E:\spilder\country_medical_insurance\country_medical_insurance\exception\exeu.ext")
        return item

    def process_country_medicine(self, item):
        print("-----------------------处理国产药品------------------")
        title = ["批准文号", "产品名称", "英文名称", "商品名", "剂型", "规格", "生产单位", "生产地址", "产品类别", "批准日期",
                 "原批准文号", "药品本位码", "药品本位码备注"]
        try:
            writeDataIntoExcel(data=item["info"], tilte=title, fileName=setting.get("COUNTRY_MEDICINE_FILE"))
            print("------------国产药品写入文件成功--------")
        except BaseException as e:
            print("国产药品写入文件异常-------{}".format(e))
            writeFile(url=item["url"], fileName=setting.get("FAIL_LOG_PATH"))


    def process_foreige_medicine(self, item):
        print("-----------------------处理进口药品------------------")
        title = ["注册证号", "原注册证号", "注册证号备注", "分包装批准文号", "公司名称（中文）", "公司名称（英文）",
                 "地址（中文）", "地址（英文）", "国家/地区（中文）", "国家/地区（英文）", "产品名称（中文）",
                 "产品名称（英文）", "商品名（中文）", "商品名（英文）", "剂型（中文）", "规格（中文）", "包装规格（中文）",
                 "生产厂商（中文）", "生产厂商（英文）", "厂商地址（中文）", "厂商地址（英文）", "厂商国家/地区（中文）",
                 "厂商国家/地区（英文）", "发证日期	", "有效期截止日", "分包装企业名称", "分包装企业地址", "分包装文号批准日期",
                 "分包装文号有效期截止日", "产品类别", "药品本位码", "药品本位码备注	"]
        try:
            writeDataIntoExcel(data=item["info"], tilte=title,fileName=setting.get("FOREIGE_MEDICINE_FILE"))
            print("------------国产药品写入文件成功--------")
        except BaseException as e:
            print("国产药品写入文件异常-------{}".format(e))
            writeFile(url=item["url"], fileName=setting.get("FAIL_LOG_PATH"))




