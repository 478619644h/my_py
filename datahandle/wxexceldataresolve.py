import csv
import os

from datahandle.dbopration import DB


def insertWXCsv(data):
    trading_hour        = str(data[0]).strip()
    trading_type        = str(data[1]).strip()
    counterparty        = str(data[2]).strip()
    commodity           = str(data[3]).strip().replace("'","\\'")
    income_and_expenses = str(data[4]).strip()
    order_amount        = str(data[5]).strip().replace("¥",'')
    payment             = str(data[6]).strip()
    current_state       = str(data[7]).strip()
    bill_order_no       = str(data[8]).strip()
    merchants_order_no  = str(data[9]).strip()
    remark              = str(data[10]).strip()
    sql = "insert into account_bill_chat(trading_hour,trading_type,counterparty,commodity,income_and_expenses,order_amount," \
          "payment,current_state,bill_order_no,merchants_order_no,remark)values('%s','%s','%s',\'%s\','%s',%s,'%s','%s','%s'," \
          "'%s','%s')"%(trading_hour,trading_type,counterparty,commodity,income_and_expenses,order_amount,\
          payment,current_state,bill_order_no,merchants_order_no,remark)

    print(sql)
    with DB() as db:
        try:
            db.execute(sql)
        except:
            db.rollback()

# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        print('--------------------------------------------------------'+child)
        output(child)


def output(path):
    #打开文件，用with打开可以不用去特意关闭file了，python3不支持file()打开文件，只能用open()
    with open(path,"r") as csvfile:
          #读取csv文件，返回的是迭代类型
          read = csv.reader(csvfile)
          for i in read:
              if len(i) > 10 and str(i[0]).strip() != "交易时间":
                insertWXCsv(i)

#with DB() as db:
    #db.execute("delete from account_bill_chat")
eachFile('../wxcsvfile/')