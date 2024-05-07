#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：B00316 
@File    ：app.py
@Author  ：MoJeffrey
@Date    ：2023/4/15 19:21 
"""

from flask import Flask, render_template, request
import pymysql
import config
import threading
from loguru import logger
from dbutils.pooled_db import PooledDB


sql_config = {
    "host": config.HOST,
    "port": config.PORT,
    "user": config.USERNAME,
    "passwd": config.PASSWORD,
    "db": config.DATABASE
}
pool = PooledDB(pymysql, config.maxConnections, **sql_config)

app = Flask(__name__)


def RunSQL(SQL):
    conn = pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    while True:
        try:
            cursor.execute(SQL)
            conn.commit()
            break
        except Exception as error:
            conn.ping(True)

    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@app.route('/')
def hello_world():
    """
    首页
    获取数据库中各人的投票数
    :return:
    """
    SQL = """
    SELECT C.id, C.name, IF(V.Num IS NULL, 0, V.Num) AS Num FROM candidate AS C
    LEFT JOIN (SELECT candidateId, COUNT(candidateId) AS Num FROM vote GROUP BY candidateId) AS V ON C.id = V.candidateId;
    """

    result = RunSQL(SQL)
    return render_template('index.html', data=result)


@app.route('/hi', methods=["POST"])
def hi():
    return 'hi'


@app.route('/vote', methods=["POST"])
def vote():
    """
    投票
    1. 判断是否有ip
    2. 判断是否有参选人id
    3. 查看数据库中是否有该ip （防刷票）
    4. 储存
    :return:
    """
    if 'id' not in request.json:
        return {
            "msg": "错误！"
        }

    ip = request.headers['X-Forwarded-For'] if 'X-Forwarded-For' in request.headers else request.remote_addr
    candidateId = request.json.get('id')

    if candidateId is None:
        return {
            "msg": "未选择投票对象！"
        }

    SQL = f"CALL vote('{ip}', '{candidateId}');"
    result = RunSQL(SQL)[0]

    if result['code']:
        msg = "ok"
    else:
        msg = "抱歉只能投一次票！"

    return {
        "msg": msg
    }

if __name__ == '__main__':
    app.run(port=80)