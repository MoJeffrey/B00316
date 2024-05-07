#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：B00316 
@File    ：VotingResults.py
@Author  ：MoJeffrey
@Date    ：2023/4/17 5:00 
"""
import re
import time

import scrapy
from ..items import WebcrawlerItem
from multiprocessing import Process, Manager


class VotingResults(scrapy.Spider):
    name = 'VotingResults'
    start_urls = []
    Num = 100
    __Delay = None
    queue = None

    def __init__(self, queue, param):
        self.__item = WebcrawlerItem()
        self.__item['now'] = {}
        self.__item['before'] = {}
        self.__item['show'] = {}

        self.start_urls = [param['URL']]
        self.__item['matplotJudgment'] = param['matplotJudgment']
        self.__Delay = param['Delay']
        self.queue = queue

    def parse(self, response):
        time.sleep(self.__Delay)

        self.Num -= 1
        if self.Num == 0:
            return

        # 获取参选者
        candidateDivList = response.xpath('//div[@class="candidate"]')
        candidateList = []
        for div in candidateDivList:
            candidate: str = div.xpath('./text()')[0].extract()
            candidate = candidate.replace(" ", '').replace('\n', '').replace('\r', '')
            candidateList.append(candidate)

        # 获取票数
        votesNumDivList = response.xpath('//div[@class="votesNum"]')
        votesNumList = []
        for div in votesNumDivList:
            votesNum: str = div.xpath('./text()')[0].extract()
            votesNum = votesNum.replace(" ", '').replace('\n', '').replace('\r', '')
            votesNumList.append(votesNum)

        # 组装数据
        self.__item['now'] = {}
        for Num in range(0, len(candidateList)):
            self.__item['now'][candidateList[Num]] = votesNumList[Num]

        yield self.__item

        self.queue.put(self.__item['show'])
        yield scrapy.Request(self.start_urls[0], callback=self.parse, dont_filter=True)