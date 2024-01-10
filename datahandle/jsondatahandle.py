from datetime import datetime
import json
import os

from datahandle.dbopration import DB


def resolveJson(path):
    file = open(path, "rb")
    fileJson = json.load(file)
    return fileJson["billPayList"]

def output(path):
    result = resolveJson(path)
    for x in result:
        # for y in x:
        #     print(y + ':' + str(x[y]))
        insertBaiTiao(x)

# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        print('--------------------------------------------------------'+child)
        output(child)


def insertBaiTiao(data):
    billName = str(data["billName"])
    amount = str(data["amount"])
    payTime = str(data["payTime"])
    with DB() as db:
        sql = "INSERT INTO account_bill_jd_baitiao(bill_name,amount,pay_time) values('%s','%s','%s')" % \
              (billName,amount,payTime)
        print(sql)
        try:
            # 执行SQL语句
            db.execute(sql)
        except:
            # 发生错误时
            db.rollback()
with DB() as db:
    db.execute("delete from account_bill_jd_baitiao")
eachFile('../jsonfile/')