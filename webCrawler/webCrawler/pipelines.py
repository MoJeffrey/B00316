#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging


class WebcrawlerPipeline:
    __logger = None

    def __init__(self):
        self.__logger = logging.getLogger()

    def ShowInit(self, info):
        self.__logger.info('开始爬取投票内')
        self.__logger.info(f'共有： {len(info.keys())} 参选')
        self.__logger.info(f'分别为： {",".join(info.keys())}')

    def ShowDifference(self, before, now, matplotJudgment) -> list:
        Candidates = before.keys()
        ChangeStringList = []
        ChangeList = []
        for Key in Candidates:
            NowNum = int(now[Key])
            BeforeNum = int(before[Key])
            if NowNum > BeforeNum:
                if (NowNum - BeforeNum) >= matplotJudgment:
                    attachString = '超过matplot规则！'
                else:
                    attachString = ''
                    ChangeList.append(Key)
                ChangeStringList.append(f"{Key} : {before[Key]} -> {now[Key]} {attachString}")

        if ChangeStringList:
            self.__logger.info('; '.join(ChangeStringList))
            return ChangeList
        else:
            self.__logger.info("票数没有改变")
            return []

    def process_item(self, item, spider):
        if item['before'] == {}:
            self.ShowInit(item['now'])
        else:
            ChangeList = self.ShowDifference(item['before'], item['now'], int(item['matplotJudgment']))
            for Key in ChangeList:
                item['show'][Key] = item['now'][Key]

        item['before'] = item['now']

        return item
