#!/usr/bin/python3

import threading
import time
import csv
import os
import datetime
import uuid
import csv

from datahandle.dbopration import DB

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name,path):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.path = path
    def run(self):
        print ("开始线程：" + self.name)
        output(self.path)
        print ("退出线程：" + self.name)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


total = 0
lock = threading.RLock();
def output(path):
    #打开文件，用with打开可以不用去特意关闭file了，python3不支持file()打开文件，只能用open()
    with open(path,"r") as csvfile:
          #读取csv文件，返回的是迭代类型
          read = csv.reader(csvfile)
          for row in read:
              print(row)
              garden     = str(row[6]).strip()
              house_num  = str(row[7]).strip()
              try:
                  lock.acquire()
                  global total
                  total = total + 1
                  print(threading.currentThread().getName())
                  print(total)
              finally:
                  lock.release()
              sqloperation(garden,house_num,30,row)
              writeCsv(row, './rightFile/dd.csv')

def sqloperation(houseName,houseNum,credit,row):
    print(houseName)
    sql = '''
    SELECT * FROM (
    SELECT hold.id,CONCAT(hold.floor_num,'-',hold.unit,'-',hold.house_num) house_num,
    members_points.id m_point_id,members_points.total_points,members.cardcode,
    members.id mid
    FROM house_holds hold join houses house on hold.h_id = house.id
    join (SELECT m.mechanism,temp.id,m.cardcode FROM members temp 
    join members m on temp.creditcard = m.id
        union
        SELECT mechanism,id,cardcode FROM members where creditcard is null) members on hold.id = members.mechanism
    join tb_members_points members_points on members_points.m_id = members.id
    WHERE house.name = '%s') temp where house_num = '%s'
    '''%(houseName,houseNum)
    with DB(host='39.106.67.154',db='garbage_sorting_sh',user='gs',passwd='fQ1M5IkxjN6W') as db:
        try:
            # 执行SQL语句
            db.execute(sql)
            for data in db.fetchall():
                print(data)
                if int(data["total_points"]) >= int(credit):

                    print(row)
                    total_credit = data["total_points"]-int(credit)
                    insetPoints(data["cardcode"],int(credit),int(data["total_points"]),total_credit,data["mid"],int(data["m_point_id"]))

                else:
                    writeCsv(row, './rightFile/ee.csv')
        except:
            # 发生错误时
            db.rollback()
#积分扣减
def insetPoints(cardCode,number,creditBefore,credit,mid,m_point_id):
    sql ='''
        INSERT INTO `points`(`uid`, `source`, `cardcode`, `type`, `number`, `reason`, 
        `credit_before`, `credit`, `created_at`, `updated_at`, `description`, `mechanism`, `mid`, `status`, 
        `refuse_reason`, `delivery_record_id`, `order_id`, `order_num`) 
        VALUES ('2c90a1706c70bc44016c89f60d1c007b', '巡检端', '%s', 1, %d, 3, %d, %d, %d, %d, NULL, 
        '40288aca6b2c2870016b2c2dcaf60002', %d, '3', NULL, NULL, NULL, NULL);
    '''%(cardCode,number,creditBefore,credit,int(time.time()),int(time.time()),mid)
    with DB(host='39.106.67.154',db='garbage_sorting_sh',user='gs',passwd='fQ1M5IkxjN6W') as db:
        try:
            db.execute(sql)
            current_id = db.lastrowid
            db.execute(insertAudit(current_id,"2c90a1706c70bc44016c89f60d1c007b"))
            db.execute(updataMemberPoints(credit,m_point_id))

        except:
            db.rollback()
    return current_id


def updataMemberPoints(credit,id):
    sql = '''
    UPDATE `tb_members_points` SET `total_points` = %d, `update_time` = now() WHERE `id` = %d    
    '''%(credit,id)
    return sql

def insertAudit(pointsId,uid):
    sql = '''
        INSERT INTO `points_auditor`(`id`, `points_id`, `status`, `remarks`, `auditor_id`,
         `create_date`) VALUES ('%s', %d, '3', '大礼包积分扣减',
          '%s', now());
    '''%(str(uuid.uuid1()).replace('-',''),pointsId,uid)
    return sql
def writeCsv(row,path):
    file = open(path,'a+')
    writer = csv.writer(file)
    writer.writerow(row)
    file.close()



# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    index = 0
    for allDir in pathDir:

        child = os.path.join('%s%s' % (filepath, allDir))
        print('--------------------------------------------------------'+child)
        myThread(index, "Thread-"+str(index), child).start()
        index = index+1
# 创建新线程
# 开启新线程
eachFile('./multXls/')
while 1:
    pass