import pymysql
from warnings import filterwarnings
from logs.logs import Logs
import threading

filterwarnings("ignore", category=pymysql.Warning)


class MYdb:
    def __init__(self):
        self.conn = pymysql.connect(host='39.99.156.212', user='root', passwd='Hao1014', database='bihu_quote',
                                    port=3306)
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.logger = Logs().logger

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def query(self, sql, fetch='all'):
        try:
            self.cur.execute(sql)
            if fetch == 'all':
                result = self.cur.fetchall()
                return result
            else:
                result = self.cur.fetchone()
                return result
        except Exception as e:
            return f"查询数据库异常：{e}"

    def execute(self, sql):
        try:
            while threading.Lock():
                self.logger.info(f"execute入参：{sql}")
                row = self.cur.execute(sql)
                self.conn.commit()
                return row
        except Exception as e:
            self.conn.rollback()
            self.logger.info(f"数据库操作异常,回滚操作。异常信息：{e}")
            return f"数据库操作异常,回滚操作。异常信息：{e}"

    def commit(self):
        self.conn.commit()
        return "执行commit"

    def begin(self):
        self.conn.begin()
        return "打开事件"


if __name__ == '__main__':
    db = MYdb()
