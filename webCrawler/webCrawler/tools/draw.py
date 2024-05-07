#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：B00316 
@File    ：draw.py
@Author  ：MoJeffrey
@Date    ：2023/4/17 7:14 
"""
import io
import operator

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from PIL import Image
from PIL.ImageQt import ImageQt

matplotlib.rc("font", family='Microsoft YaHei')

class matplotlibDraw:
    """
    主要用于画图
    """

    def __init__(self):
        matplotlib.rc("font", family='Microsoft YaHei')

    def Draw(self, quote_info: dict):
        if not quote_info:
            return None

        # 排序
        sortDia = sorted(quote_info.items(), key=operator.itemgetter(1), reverse=False)
        candidateList = []
        votesNumList = []

        for candidate, key in sortDia:
            candidateList.append(candidate)
            votesNumList.append(int(key))

        # 创建为np 数量和画图
        x = np.array(candidateList)
        y = np.array(votesNumList)

        plt.bar(x, y)
        for a, b in zip(x, y):
            plt.text(a, b, b, ha='center', va='bottom')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi = 100)
        # plt.savefig(f'{time.time()}.jpg')
        buf.seek(0)
        plt.clf()

        return ImageQt(Image.open(buf))
