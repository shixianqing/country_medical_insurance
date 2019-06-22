from country_medical_insurance.dbtool import MysqlPool
import pandas as pd


def update_hospital():
    """
        修改医院标签
    :return:
    """
    pool = MysqlPool()
    sql = '''
        update
            base_hospital
        set
            hospital_grade = %s,
            update_time = now()
        where 
            hospital_code = %s
    '''
    hospitals = pd.read_excel('上海医院等级.xlsx', sheet_name="更新", converters={u'医院码': str, u'爬虫等级': int})
    index = hospitals.index.size
    paramsList = list()
    for i in range(index):
        paramsDict = list()
        val = hospitals.ix[i]['爬虫等级']
        code = hospitals.ix[i]['医院码']
        paramsDict.append(str(val))
        paramsDict.append(str(code))
        paramsList.append(tuple(paramsDict))
    total = len(paramsList)
    pageSize = 100
    totalPages = int(total / pageSize)
    totalPages = totalPages + (0 if (total % pageSize == 0) else 1)
    print("totalPages : {}".format(totalPages))

    for pageNo in range(totalPages):
        startIndex = pageNo * pageSize
        endIndex = pageNo * pageSize + pageSize
        params = paramsList[startIndex:endIndex]
        print("数据大小：{}".format(len(params)))
        try:
            pool.batchUpdate(sql, params)
            print("第{}页数据更新完成".format(pageNo + 1))
            pool.end()
        except Exception as e:
            print("报错了")
            pool.dispose(isEnd=0)
            raise e


def update_charge_ratio():
    """
       修改医保比例
        :return:
   """
    pool = MysqlPool()
    sql = '''
        update
            base_charge_ratio
        set
            ratio = %s,
            update_time = now()
        where 
            charge_item_code = %s and 
            region_id = %s
    '''
    ratios = pd.read_excel('上海比例更新.xlsx', converters={u'项目代码': str, u'地区代码': str})
    index = ratios.index.size
    paramsList = list()
    for i in range(index):
        paramsDict = list()
        paramsDict.append(str(ratios.ix[i]['比例']))
        # lev = str(ratios.ix[i]['医保等级'])
        # paramsDict.append(None if lev == 'nan' else lev)
        paramsDict.append(str(ratios.ix[i]['项目代码']))
        paramsDict.append(str(ratios.ix[i]['地区代码']))
        print(tuple(paramsDict))
        paramsList.append(tuple(paramsDict))

    total = len(paramsList)
    pageSize = 100
    totalPages = int(total / pageSize)
    totalPages = totalPages + (0 if (total % pageSize == 0) else 1)
    print("totalPages : {}".format(totalPages))

    for pageNo in range(totalPages):
        startIndex = pageNo * pageSize
        endIndex = pageNo * pageSize + pageSize
        params = paramsList[startIndex:endIndex]
        print("数据大小：{}".format(len(params)))
        try:
            pool.batchUpdate(sql, params)
            print("第{}页数据更新完成".format(pageNo + 1))
            pool.end()
        except Exception as e:
            pool.dispose(isEnd=0)
            raise e


def exportData():
    pool = MysqlPool()
    sql = '''
             SELECT  m.drug_code,m.drug_component,m.drug_name,m.drug_form,c.medicare_level,c.ratio FROM
            base_medicine m,base_charge_ratio c
            WHERE m.drug_code = c.charge_item_code AND
            (m.drug_name LIKE %s or m.drug_component LIKE %s) 
            AND c.region_id = 310100
    '''

    drug = pd.read_excel("测试.xlsx", sheet_name="定点药品")
    #

    index = drug.index.size
    contains = dict()
    result_drug_component_arr = list()
    result_drug_name_arr = list()
    result_drug_form_arr = list()
    result_medicare_level_arr = list()
    result_ratio_arr = list()
    result_code_arr = list()

    drug_name_arr = list()
    drug_form_arr = list()
    medicare_level_arr = list()
    ratio_arr = list()
    for i in range(index):
        print("开始进行第{}行数据处理".format(i))
        drugName = drug.ix[i]['药品名']
        drugForm = drug.ix[i]['剂型']
        medicalLev = drug.ix[i]['甲乙类']
        ratio = drug.ix[i]['支付']

        args = '%' + drugName + '%'
        paramsDict = list()
        paramsDict.append(args)
        paramsDict.append(args)
        datas = pool.getAll(sql=sql, param=tuple(paramsDict))
        if datas:
            processData(datas, result_drug_component_arr, result_drug_name_arr,
                        result_drug_form_arr, result_medicare_level_arr, result_ratio_arr,result_code_arr)
            for index in range(len(datas)):
                drug_name_arr.append(drugName)
                drug_form_arr.append(drugForm)
                medicare_level_arr.append(medicalLev)
                ratio_arr.append(ratio)
        else:
            drug_name_arr.append(drugName)
            drug_form_arr.append(drugForm)
            medicare_level_arr.append(medicalLev)
            ratio_arr.append(ratio)
            result_drug_component_arr.append('')
            result_drug_name_arr.append('')
            result_drug_form_arr.append('')
            result_medicare_level_arr.append('')
            result_ratio_arr.append('')
            result_code_arr.append('')

    contains["爬虫药品名称"] = drug_name_arr
    contains["剂型"] = drug_form_arr
    contains["甲乙类"] = medicare_level_arr
    contains["支付比例"] = ratio_arr
    contains["知识库药品成分"] = result_drug_component_arr
    contains["项目名称"] = result_drug_name_arr
    contains["知识库剂型"] = result_drug_form_arr
    contains["医保分类"] = result_medicare_level_arr
    contains["自付比例"] = result_ratio_arr
    contains["药品码"] = result_code_arr
    df = pd.DataFrame(data=contains)
    writer = pd.ExcelWriter("C:\\Users\\shixianqing\\Desktop\\out.xlsx")
    df.to_excel(writer)
    writer.save()


def processData(data, result_drug_component_arr, result_drug_name_arr,
                result_drug_form_arr, result_medicare_level_arr, result_ratio_arr, result_code_arr):
    for val in data:
        drug_component = val['drug_component']
        drug_name = val['drug_name']
        drug_form = val['drug_form']
        medicare_level = val['medicare_level']
        ratio = val['ratio']
        code = val['drug_code']
        result_drug_component_arr.append(drug_component)
        result_drug_name_arr.append(drug_name)
        result_drug_form_arr.append(drug_form)
        result_medicare_level_arr.append('' if medicare_level is None else medicare_level)
        result_ratio_arr.append(str(ratio))
        result_code_arr.append(str(code))


def un_match_data():
    pool = MysqlPool()
    sql = '''
    
            SELECT  m.drug_code,m.drug_component,m.drug_name,m.drug_form,c.medicare_level,c.ratio FROM
            base_medicine m,base_charge_ratio c
            WHERE m.drug_code = c.charge_item_code
            AND c.region_id = 310100
    
    '''
    baseDatas = pool.getAll(sql=sql)

    drugNames = pd.read_excel("out.xlsx", sheet_name="Sheet1")["项目名称"].values
    drugNames = set(drugNames)
    print(len(drugNames))
    contains = dict()
    result_drug_component_arr = list()
    result_drug_name_arr = list()
    result_drug_form_arr = list()
    result_medicare_level_arr = list()
    result_ratio_arr = list()
    result_code_arr = list()
    for data in baseDatas:
        drug_name = data['drug_name']
        drug_component = data['drug_component']
        drug_form = data['drug_form']
        medicare_level = data['medicare_level']
        ratio = data['ratio']
        code = data['drug_code']
        if drug_name not in drugNames:
            print("{}没有匹配到".format(drug_name))
            result_drug_component_arr.append(drug_component)
            result_drug_name_arr.append(drug_name)
            result_drug_form_arr.append(drug_form)
            result_medicare_level_arr.append('' if medicare_level is None else medicare_level)
            result_ratio_arr.append(str(ratio))
            result_code_arr.append(str(code))

    contains["知识库药品成分"] = result_drug_component_arr
    contains["项目名称"] = result_drug_name_arr
    contains["知识库剂型"] = result_drug_form_arr
    contains["医保分类"] = result_medicare_level_arr
    contains["自付比例"] = result_ratio_arr
    contains["药品码"] = result_code_arr
    df = pd.DataFrame(data=contains)
    writer = pd.ExcelWriter("C:\\Users\\shixianqing\\Desktop\\unMatch.xlsx")
    df.to_excel(writer)
    writer.save()

def main():
    # update_charge_ratio()
    # update_hospital()
    exportData()
    # un_match_data()

if __name__ == '__main__':
    main()
