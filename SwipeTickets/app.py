#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：B00316 
@File    ：app.py
@Author  ：MoJeffrey
@Date    ：2023/4/16 3:05 
"""
import random
import time

import requests
import config
import multiprocessing as mp
from loguru import logger
from lxml import etree


def Veto(CandidatesNum: int):
    """
    Post 一个投票请求
    :return:
    """
    CandidateId = random.randint(1, CandidatesNum)
    jsonData = {
        "id": CandidateId
    }
    headers = {
        "Content-Type": 'application/json',
        "X-Forwarded-For": randomIp()
    }
    res = requests.post(config.URL + '/vote', json=jsonData, headers=headers)
    if res.status_code == 200:
        return CandidateId
    else:
        return None


def GetCandidateList() -> list:
    res = requests.get(config.URL)
    response = etree.HTML(res.content)
    # 获取参选者
    candidateDivList = response.xpath('//div[@class="candidate"]')
    candidateList = []
    for div in candidateDivList:
        candidate: str = div.xpath('./text()')[0]
        candidate = candidate.replace(" ", '').replace('\n', '').replace('\r', '')
        candidateList.append(candidate)
    return candidateList


def randomIp() -> str:
    """
    随机生成一个IP
    :return:
    """
    m = random.randint(0, 255)
    n = random.randint(0, 255)
    x = random.randint(0, 255)
    y = random.randint(0, 255)
    return f'{m}.{n}.{x}.{y}'

def More(CandidateList):
    # 电脑核心数量
    num_cores = int(mp.cpu_count())
    pool = mp.Pool(num_cores - 1)
    logger.success(f"开始刷票， 核心数{num_cores}")
    while True:
        results = []
        for Num in range(0, num_cores):
            results.append(pool.apply_async(Veto, args=(len(CandidateList), )))
        results = [p.get() for p in results]
        Print(CandidateList, results)
        time.sleep(config.Sleep)

def OnlyOne(CandidateList):
    while True:
        results = Veto(len(CandidateList))
        Print(CandidateList, [results])
        time.sleep(config.Sleep)

def Print(CandidateList, results):
    data = [0] * len(CandidateList)
    PrintStringList = []
    for Item in results:
        data[Item - 1] += 1

    for Num in range(0, len(data)):
        PrintStringList.append(f"{CandidateList[Num]}:{data[Num]}票 ")

    logger.success(';'.join(PrintStringList))

if __name__ == '__main__':
    More(GetCandidateList())
    # OnlyOne()