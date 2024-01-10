import psycopg2

class SqlConn():
    '''
    连接数据库，以及进行一些操作的封装
    '''
    database = ''
    user = ''
    password = ''
    port = 0
    host = ''

    # 创建连接、游标
    def __init__(self, *args, **kwargs):
        if kwargs.get("database"):
            self.database = kwargs.get("database")
        if kwargs.get("user"):
            self.user = kwargs.get("user")
        if kwargs.get("password"):
            self.password = kwargs.get("password")
        if kwargs.get("port"):
            self.port = kwargs.get("port")
        if kwargs.get("host"):
            self.host = kwargs.get("host")

        if not (self.host and self.port and self.user and
                self.password and self.database):
            raise Warning("conn_error, missing some params!")

        sql_conn = {
                    'postgresql': psycopg2
                    }

        self.conn = sql_conn[self.sql_name].connect(host=self.host,
                                                    port=self.port,
                                                    user=self.user,
                                                    password=self.password,
                                                    database=self.database,
                                                    )
        self.cursor = self.conn.cursor()
        if not self.cursor:
            raise Warning("conn_error!")

    # 测试连接
    def test_conn(self):
        if self.cursor:
            print("conn success!")
        else:
            print('conn error!')

    # 单条语句的并提交
    def execute(self, sql_code):
        self.cursor.execute(sql_code)
        self.conn.commit()

    # 单条语句的不提交
    def execute_no_conmmit(self, sql_code):
        self.cursor.execute(sql_code)

    # 构造多条语句，使用%s参数化，对于每个list都进行替代构造
    def excute_many(self, sql_base, param_list):
        self.cursor.executemany(sql_base, param_list)

    # 批量执行（待完善）
    def batch_execute(self, sql_code):
        pass

    # 获取数据
    def get_data(self, sql_code, count=0):
        self.cursor.execute(sql_code)
        if int(count):
            return self.cursor.fetchmany(count)
        else:
            return self.cursor.fetchall()

    # 更新数据
    def updata_data(self, sql_code):
        self.cursor(sql_code)

    # 插入数据
    def insert_data(self, sql_code):
        self.cursor(sql_code)

    # 滚动游标
    def cursor_scroll(self, count, mode='relative'):
        self.cursor.scroll(count, mode=mode)

    # 提交
    def commit(self):
        self.conn.commit()

    # 回滚
    def rollback(self):
        self.conn.rollback()

    # 关闭连接
    def close_conn(self):
        self.cursor.close()
        self.conn.close()