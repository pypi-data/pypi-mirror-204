# -*- coding: utf-8 -*-
# @Time    : 2023/4/23 17:18:24
# @Author  : Pane Li
# @File    : inmongodb.py
"""
inmongodb

"""
import logging
from pymongo import MongoClient


class Mongodb:
    """mongodb数据库操作类"""

    def __init__(self, host: str, port: int, user: str = None, password: str = None):
        """
        初始化
        :param host: 主机
        :param port: 端口
        :param user: 用户名
        :param password: 密码
        """

        self.client = MongoClient(host, port, username=user, password=password)

    def insert(self, db: str, collection: str, data: dict):
        """
        插入数据
        :param db: 数据库
        :param collection: 集合
        :param data: 数据
        :return:
        """
        self.client[db][collection].insert_one(data)
        logging.info('insert data success')

    # 删除数据
    def delete(self, db: str, collection: str, data: dict):
        """
        删除数据
        :param db: 数据库
        :param collection: 集合
        :param data: 数据
        :return:
        """
        self.client[db][collection].delete_one(data)
        logging.info('delete data success')

    # 插入多条数据
    def insert_many(self, db: str, collection: str, data: list):
        """
        插入多条数据
        :param db: 数据库
        :param collection: 集合
        :param data: 数据
        :return:
        """
        self.client[db][collection].insert_many(data)
        logging.info('insert data success')

    # 更新数据
    def update_many(self, db: str, collection: str, data: dict, new_data: dict):
        """
        更新数据
        :param db: 数据库
        :param collection: 集合
        :param data: 数据     {'name': 'liwei'}
        :param new_data: 新数据  {'$set': {'name': 'liwei111'}}
        :return:
        """
        self.client[db][collection].update_many(data, new_data)
        logging.info('update data success')

    # 聚合查询 且返回数据
    def aggregate(self, db: str, collection: str, data: list):
        """
        聚合查询
        :param db: 数据库
        :param collection: 集合
        :param data: 数据     [{'$match': {'name': 'liwei'}}]
        :return:
        """
        return list(self.client[db][collection].aggregate(data))


if __name__ == '__main__':
    mongodb = Mongodb('10.5.17.107', 27017, 'root', 'admin',)
    print(mongodb.aggregate('test', 'test', [{'$match': {'name': 'liwei111'}}]))
