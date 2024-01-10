import csv
import os
import time
import datetime
import uuid
import csv

from datahandle.dbopration import DB


# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        print('--------------------------------------------------------' + child)
        output(child)


index = 0
index2 = 0


def output(path):
    # 打开文件，用with打开可以不用去特意关闭file了，python3不支持file()打开文件，只能用open()
    with open(path, "r") as csvfile:
        # 读取csv文件，返回的是迭代类型
        read = csv.reader(csvfile)
        global index

        for row in read:
            #print(row)
            garden = str(row[2]).strip()
            house_num = str(row[3]).strip()
            credit = str(row[5]).strip()
            global index2
            index2 = index2 + 1
            # print(row)
            # print(index2)
            # print('garden:' + garden + "  " + "house_num: " + house_num )
            sqloperation(garden, house_num, credit, row)
        # print(index2)


total = 0
handle = 0
ip = '172.16.33.240'


def sqloperation(houseName, houseNum, credit, row):
    sql = '''
    SELECT * FROM (
    SELECT hold.id,CONCAT(hold.floor_num,'-',hold.unit,'-',hold.house_num) house_num,
    members_points.id m_point_id,members_points.total_points,members.cardcode,
    members.id mid
    FROM house_holds hold join houses house on hold.h_id = house.id
    join (SELECT m.mechanism,temp.id,m.cardcode FROM members temp 
    join members m on temp.creditcard = m.id
		union all
		SELECT mechanism,id,cardcode FROM members where creditcard is not null ) members on hold.id = members.mechanism
    join tb_members_points members_points on members_points.m_id = members.id
    WHERE house.name = '%s') temp where house_num = '%s'
    ''' % (houseName, houseNum)
    with DB(host=ip, db='garbage_sorting_sh', user='gs', passwd='fQ1M5IkxjN6W') as db:
        try:
            # 执行SQL语句
            db.execute(sql)
            for data in db.fetchall():
                global total
                total = total + 1
                if int(data["total_points"]) >= int(credit):
                    print(row)
                    # total_credit = data["total_points"]-int(credit)
                    # insetPoints(data["cardcode"],int(credit),int(data["total_points"]),total_credit,data["mid"],int(data["m_point_id"]))
                    # writeCsv(row,'./rightFile/cc.csv')
                    # total = total + 1
                    # print(total)

        except:
            # 发生错误时
            db.rollback()


# 积分扣减
def insetPoints(cardCode, number, creditBefore, credit, mid, m_point_id):
    sql = '''
        INSERT INTO `points`(`uid`, `source`, `cardcode`, `type`, `number`, `reason`, 
        `credit_before`, `credit`, `created_at`, `updated_at`, `description`, `mechanism`, `mid`, `status`, 
        `refuse_reason`, `delivery_record_id`, `order_id`, `order_num`) 
        VALUES ('2c90a1706c70bc44016c89f60d1c007b', '巡检端', '%s', 1, %d, 3, %d, %d, %d, %d, NULL, 
        '40288aca6b2c2870016b2c2dcaf60002', %d, '3', NULL, NULL, NULL, NULL);
    ''' % (cardCode, number, creditBefore, credit, int(time.time()), int(time.time()), mid)
    with DB(host='39.106.67.154', db='garbage_sorting_sh', user='gs', passwd='fQ1M5IkxjN6W') as db:
        try:
            db.execute(sql)
            current_id = db.lastrowid
            db.execute(insertAudit(current_id, "2c90a1706c70bc44016c89f60d1c007b"))
            db.execute(updataMemberPoints(credit, m_point_id))

        except:
            db.rollback()
    return current_id


# 积分增加
def insetPointsOfAdd(cardCode, number, creditBefore, credit, mid, m_point_id, org_id, uid):
    sql = '''
        INSERT INTO `points`(`uid`, `source`, `cardcode`, `type`, `number`, `reason`, 
        `credit_before`, `credit`, `created_at`, `updated_at`, `description`, `mechanism`, `mid`, `status`, 
        `refuse_reason`, `delivery_record_id`, `order_id`, `order_num`) 
        VALUES ('%s', '巡检端', '%s', 0, %d, 3, %d, %d, 1420041600, 1420041600, NULL, 
        '%s', %d, '3', NULL, NULL, NULL, NULL);
    ''' % (uid, cardCode, number, creditBefore, credit, org_id, mid)
    with DB(host='39.106.67.154', db='garbage_sorting_sh', user='gs', passwd='fQ1M5IkxjN6W') as db:
        try:
            db.execute(sql)
            current_id = db.lastrowid
            db.execute(insertAudit(current_id, uid))
            db.execute(updataMemberPoints(credit, m_point_id))

        except:
            db.rollback()
    return current_id


def updataMemberPoints(credit, id):
    sql = '''
    UPDATE `tb_members_points` SET `total_points` = %d, `update_time` = now() WHERE `id` = %d    
    ''' % (credit, id)
    return sql


def insertAudit(pointsId, uid):
    sql = '''
        INSERT INTO `points_auditor`(`id`, `points_id`, `status`, `remarks`, `auditor_id`,
         `create_date`) VALUES ('%s', %d, '3', '大礼包积分扣减',
          '%s', now());
    ''' % (str(uuid.uuid1()).replace('-', ''), pointsId, uid)
    return sql


def writeCsv(row, path):
    file = open(path, 'a+')
    writer = csv.writer(file)
    writer.writerow(row)
    file.close()


##################################################################################
# 处理积分有负数的情况
def queryTbMembersPoints():
    sql = '''
    SELECT 
		hold.id,
        members_points.id m_point_id,
		members_points.total_points,
		members_points.org_id,
		members.cardcode,
        members.id mid
    FROM house_holds hold 
		join (
		SELECT m.mechanism,temp.id,m.cardcode FROM members temp 
    join members m on temp.creditcard = m.id
		union all
		SELECT mechanism,id,cardcode FROM members where creditcard is null
		) members on members.mechanism = hold.id
    join tb_members_points members_points on members_points.m_id = members.id
   where members_points.total_points < 0 
    '''
    with DB(host='39.106.67.154', db='garbage_sorting_sh', user='gs', passwd='fQ1M5IkxjN6W') as db:
        try:
            db.execute(sql)
            for data in db.fetchall():
                m_point_id = data["m_point_id"]
                total_point = data["total_points"]
                cardcode = str(data["cardcode"]).strip()
                mid = data["mid"]
                org_id = data["org_id"]
                if total_point < 0:
                    uid = ""
                    if org_id == "40288aca6b2c2870016b2c2dcaf60002":
                        uid = "2c90a1706c70bc44016c89f60d1c007b"
                    if org_id == "40288aca6b2bfac9016b2c1d32c60002":
                        uid = "2c90a17071552aa601715c62849e0116"
                    if len(uid) < 2:
                        print("##########################")
                    insetPointsOfAdd(cardcode, -total_point, total_point, 0, int(mid), m_point_id, org_id, uid)
                    writeCsv([org_id, mid, cardcode, total_point, m_point_id], './rightFile/bb.csv')
        except:
            db.rollback()

if __name__ == "__main__":
    eachFile('./xlsFile/')

