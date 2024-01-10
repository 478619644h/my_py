import csv
import os
import threading

import requests

from datahandle.dbopration import DB
from my_logger import logger

ip = '172.16.33.240'
domain = "http://st.haoleiok.com:8082/garbagesort/"
url="houseHoldsController.do?doDel&id=%d"
total = 0
header={
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection':'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':'i18n_browser_Lang=zh-cn; JEECGINDEXSTYLE=hplus; JSESSIONID=1373167886EAD8FA5ED0A7473A0E4202; Hm_lvt_098e6e84ab585bf0c2e6853604192b8b=1609301596,1610606614,1611195959,1611558475; ZINDEXNUMBER=1990; Hm_lpvt_098e6e84ab585bf0c2e6853604192b8b=1611638280',
    'Host': 'st.haoleiok.com:8082',
    'Origin': 'http://st.haoleiok.com:8082',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50',
    'X-Requested-With': 'XMLHttpRequest'
}


#
#40288aca6b2bfac9016b2c1d32c60002 //杭州桑德

def queryHouseHold(floor, unit, householdNum,houses):
    sql = '''
    SELECT hh.* FROM  
    (SELECT id FROM houses h where mechanism_id = '40288aca6b2bfac9016b2c1d32c60002' and name = '%s' ) t inner join 
    house_holds hh on hh.h_id = t.id where hh.floor_num ='%s' and unit='%s' and house_num='%s'
    ''' % (houses,floor, unit, householdNum)
    with DB(host=ip, db='garbage_sorting_sh', user='gs', passwd='fQ1M5IkxjN6W') as db:
        # 执行SQL语句
        db.execute(sql)
        data = db.fetchone()
        print(data)
        if data is not None:
            delHouseholdBySql(data["id"])
            logger.info(data)
            writeCsv([floor,unit,householdNum,data["id"]])


def readCsv(dir,houses):
    filePath = os.path.join("%s%s"%("./csvFile/",dir))
    with open(filePath,"r") as file:
        read = csv.reader(file)
        for row in read:
            floor=str(row[0])
            unit=str(row[1])
            household_num=str(row[2])
            queryHouseHold(floor,unit,household_num,houses)

def delHouseholdBySql(household_id):
    tb_home_rfid = "delete from tb_home_rfid where hld_id =%d;"%(household_id)
    members = "delete from members where mechanism =%d;"%(household_id)
    tb_households_month_count = "delete from tb_households_month_count where hhid =%d;"%(household_id)
    tb_households_sevendays_count = "delete from tb_households_sevendays_count where hhid =%d;"%(household_id)
    tb_households_thismonth_count = "delete from tb_households_thismonth_count where hhid=%d;"%(household_id)
    household = "delete from house_holds where id=%d;"%(household_id)
    #execute_sql = tb_home_rfid+members+tb_households_month_count+tb_households_sevendays_count+tb_households_thismonth_count+household
    with DB(host=ip, db='garbage_sorting_sh', user='gs', passwd='fQ1M5IkxjN6W') as db:
        # 执行SQL语句
        db.execute(tb_home_rfid)
        db.execute(members)
        db.execute(tb_households_month_count)
        db.execute(tb_households_sevendays_count)
        db.execute(tb_households_thismonth_count)
        db.execute(household)



def delHouseholdByHTTP(household_id):
    responseJson = None
    with requests.get(domain+url%(household_id),headers=header) as r:
        global total
        if r.status_code != 200:
            print("响应错误 程序退出")
            return
        total = total + 1
        print(total)
        print(r.text)
        responseJson = r.json()
    if '户室下有厨余信息，不能删除！' == responseJson["msg"]:
        return False
    return True

def writeCsv(row, path="./un_handle.csv"):
    file = open(path, 'a+')
    writer = csv.writer(file)
    writer.writerow(row)
    file.close()

class myThread (threading.Thread):
    def __init__(self, threadID, name,path,houses):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.path = path
        self.houses = houses
    def run(self):
        print ("开始线程：" + self.name)
        readCsv(self.path,self.houses)
        print ("退出线程：" + self.name)



if __name__ == "__main__":
    myThread(1, "Thread-" + str(1), "副本柏峰珑悦府需删除.csv","柏峰珑悦府").start()
    #myThread(2, "Thread-" + str(2), "副本湖滨花园需删除.csv","湖滨花园").start()
    #myThread(3, "Thread-" + str(3), "guangze.csv", "广泽小区").start()
    #myThread(4, "Thread-" + str(4), "guanze1.csv", "广泽小区").start()