import pymysql

class DB():
    def __init__(self, host='localhost', port=3306, db='my_life', user='huangyujian', passwd='huangyujian', charset='utf8mb4'):
        # 建立连接
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        # 创建游标，操作设置为字典类型
        self.cur = self.conn.cursor(cursor = pymysql.cursors.DictCursor)

    def __enter__(self):
        # 返回游标
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交数据库并执行
        self.conn.commit()
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def rollback(self):
        self.rollback();


if __name__ == '__main__':
    with DB(user='huangyujian',passwd='huangyujian',db='test') as db:
        db.execute('select * from test')
        print(db)
        for i in db:
            print(i)