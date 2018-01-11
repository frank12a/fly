from utils.pool import db_pool
import pymysql

class SQLHelper(object):
    ''''
    连接数据库
    '''

    def __init__(self):
        '''初始化'''
        self.conn = None
        self.cursor = None

    def open(self,cursor=pymysql.cursors.DictCursor):
        '''连接数据库与建立游标连接'''
        self.conn = db_pool.POOL.connection()
        self.cursor = self.conn.cursor(cursor=cursor)#数据是字典类型啦

    def close(self):
        '''关闭游标连接与数据库连接'''
        self.cursor.close()
        self.conn.close()

    def fetchone(self,sql,params):
        '''获取单个数据'''
        cursor = self.cursor
        cursor.execute(sql,params)
        result = cursor.fetchone()
        return result
    def add(self,sql, params):
        cursor = self.cursor
        cursor.execute(sql, params)
        self.conn.commit()
        # result = cursor.fetchall()
        return True
    def fetchall(self, sql, params):
        '''获取所有的数据'''
        cursor = self.cursor
        cursor.execute(sql, params)
        result = cursor.fetchall()
        return result

    def __enter__(self):
        '''上下文进入使用'''

        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''上下文推出使用'''
        self.close()

# with SQLHelper() as obj:
#
#     print(obj)
#     print('正在执行')