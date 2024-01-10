
import uuid
import time
from datahandle.dbopration import DB
from my_logger import logger

#积分的增加 or 减少 数据来源 database
#获取members积分信息
'''
INSERT INTO temp_credit_handle (SELECT * FROM (
SELECT    
m.id,
m.cardcode,
h.`name`, 
CONCAT( hh.floor_num, '-', hh.unit, '-', hh.house_num ) household, 
p.total_points credit,
p.id m_point_id
					FROM members m  
					INNER JOIN house_holds hh ON m.mechanism = hh.id  
					INNER JOIN houses h ON hh.h_id = h.id 
				  INNER JOIN ( SELECT c.id cid,m.id mid,m.mobile
					FROM  ( SELECT id, creditcard, mobile FROM members WHERE creditcard IS NOT NULL ) m 
					right JOIN ( SELECT id FROM members m WHERE mechanism IS NOT NULL ) c ON m.creditcard = c.id 
					) me ON me.cid = m.id  
					LEFT JOIN tb_members_points p ON p.m_id = IFNULL(me.mid ,me.cid) and p.org_id=h.mechanism_id
) temp where temp.name in ('崇化小区','崇化住宅区') and temp.credit > 0
					 )
'''


ip = '172.16.33.240'
handleTotal = 0
def queryNecessaryHandle():
    sql = '''
    SELECT * FROM temp_credit_handle where is_handled = 0
    '''
    with DB(host=ip, db='garbage_sorting_sh', user='gs', passwd='fQ1M5IkxjN6W') as db:
        try:
            # 执行SQL语句
            db.execute(sql)
            for data in db.fetchall():
                global handleTotal
                handleTotal = handleTotal + 1

                if data["current_credit"] is None:
                    continue

                num = int(data["credit"]) #待扣减积分
                current_credit = int(data["current_credit"])#总积分
                # insetPointsOfAdd(data["cardcode"],
                #                  int(data["credit"]), #num
                #                  int(data["current_credit"]),
                #                  int(data["current_credit"])+int(data["credit"]),
                #                  data["id"],
                #                  data["member_points_id"],
                #                  str(data["org_id"]),
                #                  "2c90a170754df6520175d9ca17210ee1")


                if current_credit >= num:
                    insetPoints(data["cardcode"],
                                num,
                                current_credit,
                                int(data["current_credit"])-int(data["credit"]),
                                data["id"],
                                int(data["member_points_id"]),
                                str(data["org_id"]),
                                '2c90a1706c70bc44016c89f60d1c007b')
                db.execute("update temp_credit_handle set is_handled = 1 where id = %d"%(int(data["id"])))
            print("共处理了：[%s]条数据"%(handleTotal))
        except:
            # 发生错误时
            db.rollback()

# 积分扣减
def insetPoints(cardCode, number, creditBefore, credit, mid, m_point_id,orgId,uid):
    sql = '''
        INSERT INTO `points`(`uid`, `source`, `cardcode`, `type`, `number`, `reason`, 
        `credit_before`, `credit`, `created_at`, `updated_at`, `description`, `mechanism`, `mid`, `status`, 
        `refuse_reason`, `delivery_record_id`, `order_id`, `order_num`) 
        VALUES ('%s', '巡检端', '%s', 1, %d, 3, %d, %d, %d, %d, NULL, 
        '%s', %d, '3', NULL, NULL, NULL, NULL);
    ''' % (uid,cardCode, number, creditBefore, credit, int(time.time()), int(time.time()),orgId,mid)
    with DB(host=ip, db='garbage_sorting_sh', user='gs', passwd='fQ1M5IkxjN6W') as db:
        try:
            logger.info(sql)
            db.execute(sql)
            current_id = db.lastrowid

            insertAuditsql = insertAudit(current_id, uid)
            logger.info(insertAuditsql)
            db.execute(insertAuditsql)

            updataMemberPointssql = updataMemberPoints(credit, m_point_id)
            logger.info(updataMemberPointssql)
            db.execute(updataMemberPointssql)

        except:
            db.rollback()
    return current_id

# 积分增加
def insetPointsOfAdd(cardCode, number, creditBefore, credit, mid, m_point_id, org_id, uid):
    sql = '''
        INSERT INTO `points`(`uid`, `source`, `cardcode`, `type`, `number`, `reason`, 
        `credit_before`, `credit`, `created_at`, `updated_at`, `description`, `mechanism`, `mid`, `status`, 
        `refuse_reason`, `delivery_record_id`, `order_id`, `order_num`) 
        VALUES ('%s', '巡检端', '%s', 0, %d, 3, %d, %d, %d, %d, NULL, 
        '%s', %d, '3', NULL, NULL, NULL, NULL);
    ''' % (uid, cardCode, number, creditBefore, credit,int(time.time()), int(time.time()), org_id, mid)
    with DB(host=ip, db='garbage_sorting_sh', user='gs', passwd='fQ1M5IkxjN6W') as db:
        try:
            logger.info(sql)
            db.execute(sql)


            current_id = db.lastrowid
            insert_audit_sql = insertAudit(current_id, uid)

            logger.info(insert_audit_sql)
            db.execute(insert_audit_sql)



            if m_point_id is None:

              insertMemberPointssql = insertMemberPoints(credit,org_id,mid)
              logger.info(insertMemberPointssql)
              db.execute(insertMemberPointssql)


            else:
              updataMemberPointsSql = updataMemberPoints(credit, int(m_point_id))
              logger.info(updataMemberPointsSql)

              db.execute(updataMemberPointsSql)



        except:
            db.rollback()
    return current_id

def updataMemberPoints(credit, id):
    sql = '''
    UPDATE `tb_members_points` SET `total_points` = %d, `update_time` = now() WHERE `id` = %d    
    ''' % (credit, id)
    return sql

def insertMemberPoints(credit, orgId,memberId):
    sql = '''
    INSERT INTO `tb_members_points`(`total_points`, `org_id`, `m_id`, `expiration_date`, `update_time`) 
    VALUES (%d, '%s', %d, NULL, now());   
    ''' % (credit,orgId,memberId)
    return sql


def insertAudit(pointsId, uid):
    sql = '''
        INSERT INTO `points_auditor`(`id`, `points_id`, `status`, `remarks`, `auditor_id`,
         `create_date`) VALUES ('%s', %d, '3', '积分扣减',
          '%s', now());
    ''' % (str(uuid.uuid1()).replace('-', ''), pointsId, uid)
    return sql
if __name__ == "__main__":
    queryNecessaryHandle()