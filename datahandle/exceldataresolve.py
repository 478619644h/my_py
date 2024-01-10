import csv
import os
from datahandle.dbopration import DB


def insertAliCsvInfo(data):
    trade_create_tiem   = str(data[2] ).strip()
    pay_time            = "'" + str(data[3] ).strip() + "'"
    if len(pay_time) < 3:
        pay_time = 'null'
    update_time         = str(data[4] ).strip()
    trade_place         = str(data[5] ).strip()
    type                = str(data[6] ).strip()
    counterparty        = str(data[7] ).strip()
    product_name        = str(data[8] ).strip()
    order_amount        = str(data[9] ).strip()
    income_and_expenses = str(data[10]).strip()
    trade_state         = str(data[11]).strip()
    service_charge      = str(data[12]).strip()
    refund_state        = str(data[13]).strip()
    remark              = str(data[14]).strip()
    fund_state          = str(data[15]).strip()
    merchants_order_no  = str(data[1] ).strip()
    bill_order_no       = str(data[0] ).strip()

    sql = "insert into account_bill_alipay(bill_order_no,merchants_order_no,trade_create_tiem,pay_time,update_time," \
          "trade_place,type,counterparty,product_name,order_amount,income_and_expenses,trade_state,service_charge,refund_state," \
          "fund_state,remark)values('%s','%s','%s',%s,'%s','%s','%s','%s',\"%s\",%s,'%s','%s','%s','%s','%s','%s')"%\
            (bill_order_no,merchants_order_no,trade_create_tiem,pay_time,update_time,\
              trade_place,type,counterparty,product_name,order_amount,income_and_expenses,trade_state,service_charge,refund_state,\
              fund_state,remark)
    print(sql)
    with DB() as db:
        try:
            # 执行SQL语句
            db.execute(sql)
        except:
            # 发生错误时
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
    with open(path,"r",encoding="gbk") as csvfile:
          #读取csv文件，返回的是迭代类型
          read = csv.reader(csvfile)
          for i in read:
              if len(i) > 15 and str(i[0]).strip() != "交易号": #列数大于15
                insertAliCsvInfo(i)

#with DB() as db:
    #db.execute("delete from account_bill_alipay")
eachFile('../alicsvfile/')