#!/usr/bin/python
# coding:utf-8

import logging

import pymysql

logger = logging.getLogger(__name__)


class DbHelper:

    def __init__(self, **kwargs):
        self.conn = pymysql.connect(**kwargs)

    def query(self, sql, args=None):
        """
        执行Sql语句
        :param sql:
        :param args:
        :return:(fields,rows )
        """
        c = self.conn.cursor()
        c.execute(sql, args)
        c.close()
        thead = [e[0] for e in c.description]
        tbody = c.fetchall()
        return thead, tbody

    def query_dict(self, sql, args=None):
        """
        执行Sql语句 返回字典
        :param sql:
        :param args:
        :return:(fields,rows )
        """
        c = self.conn.cursor(pymysql.cursors.DictCursor)
        c.execute(sql, args)
        c.close()
        datas = c.fetchall()
        return datas

    def update(self, sql, args=None):
        """
        执行Sql语句
        :param sql:
        :param args:
        """
        c = self.conn.cursor()
        try:
            i = c.execute(sql, args)
            self.conn.commit()
            return i
        except Exception as e:
            self.conn.rollback()
            # 事务回滚
            logger.error('事务处理失败', e)
            raise e
        finally:
            c.close()

    def update_many(self, sql, args):
        """
        执行Sql语句
        :param sql: 参数为tuple时用%s,为dict时用%(name)
        :param args:
        """
        c = self.conn.cursor()
        try:
            i = c.executemany(sql, args)
            self.conn.commit()
            return i
        except Exception as e:
            self.conn.rollback()
            # 事务回滚
            logger.error('事务处理失败', e)
            raise e
        finally:
            c.close()

    @staticmethod
    def map_list(fields, rows):
        datarow = []
        for row in rows:
            temp = {}
            for i, e in enumerate(fields):
                temp[e] = row[i]
            datarow.append(temp)
        return datarow
