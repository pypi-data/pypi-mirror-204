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
        thead = [e[0] for e in c.description]
        tbody = c.fetchall()
        return thead, tbody

    def query_for_map(self, sql, args=None):
        """
        执行Sql语句
        :param sql:
        :param args:
        :return:map
        """
        fields, rows = self.query(sql, args)
        return self.map_list(fields, rows)

    def update(self, sql, args=None):
        """
        执行Sql语句
        :param sql:
        :param args:
        """
        try:
            c = self.conn.cursor()
            i = c.execute(sql, args)
            self.conn.commit()
            return i
        except Exception as e:
            self.conn.rollback()
            # 事务回滚
            logger.error('事务处理失败', e)
            raise e

    @staticmethod
    def map_list(fields, rows):
        datarow = []
        for row in rows:
            temp = {}
            for i, e in enumerate(fields):
                temp[e] = row[i]
            datarow.append(temp)
        return datarow