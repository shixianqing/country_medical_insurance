from xlrd import open_workbook
from xlwt import Workbook
from xlutils.copy import copy
import os
import pandas as pd
import re

df = pd.read_excel(os.path.abspath('../form_rule.xlsx'))
rules = df.set_index('name').to_dict()['alias']


def read_time_out_url():
    lines = []
    with open("E:\\spilder\\country_medical_insurance\\country_medical_insurance\\exception\\exeu.ext") as file:
        lines = file.readlines()
        print(lines)

    return lines


def writeFile(url, fileName):
    with open(file=fileName, mode="a", encoding="utf-8") as file:
        file.write(url)
        file.write("\n")


def writeDataIntoExcel(data, tilte, fileName):
    '''
    :param data:  写入文件的数据
    :param tilte: 写入文件标题
    :param fileName: 文件名称 包含路径
    :return:
    '''

    path = fileName[:lastIndexOf(fileName, "/")]
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(fileName):
        wk = Workbook(encoding="utf-8")
        sheet = wk.add_sheet(sheetname=fileName[lastIndexOf(fileName, "/") + 1:lastIndexOf(fileName, ".")])
        if tilte:
            for i, v in enumerate(zip(tilte, data)):
                sheet.write(0, i, v[0])
                sheet.write(1, i, v[1])
        else:
            for i, v in enumerate(data):
                sheet.write(0, i, v)
        wk.save(fileName)
    else:
        wb = open_workbook(filename=fileName)
        rows = wb.sheet_by_index(0).nrows  # 获取行数， 行数的角标从0开始
        c_wb = copy(wb=wb)
        c_st = c_wb.get_sheet(0)
        for i, v in enumerate(data):
            c_st.write(rows, i, v)
        c_wb.save(fileName)


def lastIndexOf(origin_str, s):
    '''
        获取字符最后一次出现的位置
        :param strs:  源字符串
        :param s: 要定位的字符串s:
        :return:
    '''
    last_position = -1
    while True:
        positon = origin_str.find(s, last_position + 1)
        if positon == -1:
            return last_position
        last_position = positon


def getCustForm(form):
    '''
    获取自定义剂型
    :return:
    '''
    tran_form = mask_punctuation(form)
    for key, value in rules.items():
        for val in value.split('|'):
            # alias = mask_punctuation(val)
            val = val.replace('\n', '').replace('\r', '').replace('\t', '')
            if form == val or val in tran_form:
                return True, key

    return False, ''


punc_sub_pat = re.compile('[^\u4e00-\u9fa5a-zA-Z0-9]')
punc_sub_mask_digit_pat = re.compile('[^\u4e00-\u9fa5a-zA-Z]')
def mask_punctuation(w, mask_digit=False):
    if mask_digit:
        return [str for str in punc_sub_pat.sub(" ", w).split(" ") if str !='']
    else:
        return [str for str in punc_sub_mask_digit_pat.sub(" ",w).split(" ") if str !='']



def writeDataIntoTxt(data):
    with open(os.path.abspath('../manual_handler.txt'), mode='a', encoding='utf-8') as file:
        file.write('\t\t\t'.join(data))
        file.write('\n')


