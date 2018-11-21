# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import country_medical_insurance.dbtool as db
from country_medical_insurance.util.fileUtil import writeFile

class CountryMedicalInsurancePipeline(object):

    pool = db.MysqlPool()

    def process_item(self, item, spider):

        info = item["info"]
        print("info--------------->>>>{}".format(info))

        sql = "insert into country_medicine(allow_no,medicine_name,en_name,trade_name,form,medicine_size,prod_unit,prod_addr," \
              "prod_type,allow_date,origin_allow_no,medicine_ben_code,code_remark) " \
              "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        print("sql---===========>>>" + sql)
        try:
            self.pool.insert(sql, param=tuple(tuple(info)))
            self.pool.end("commit")
        except BaseException as e:
            # print(e)
            print("数据插入失败！")
            writeFile(url=item["url"], fileName="exception.txt")
        return item

class ForeigeMedicinePipeline(object):

    def process_item(self, item, spider):

        print("item----------->>>>{}".format(item["medicine_info"]))
        return item


writeFile(url="".join(tuple((1,2,3))), fileName="exception.txt")
