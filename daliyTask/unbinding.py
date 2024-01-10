from datahandle.dbopration import DB
import time

ip = '172.16.33.240'

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
            db.execute(sql)
        except:
            db.rollback()