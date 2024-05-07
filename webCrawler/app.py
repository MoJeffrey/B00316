#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：B00316 
@File    ：QTAPP.py
@Author  ：MoJeffrey
@Date    ：2023/4/18 11:08 
"""
import sys

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process, Manager
from scrapy.utils.project import get_project_settings
from webCrawler.spiders.VotingResults import VotingResults
from webCrawler.tools.draw import matplotlibDraw


def crawl(queue, param):
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl(VotingResults, queue=queue, param=param)
    process.start()


class QTAPP(QWidget):
    """
    用于显示图片
    """
    __label: QLabel = None
    __MP: matplotlibDraw = None
    __config: dict = None

    def __init__(self, config):
        super().__init__()

        self.__config = config
        self.Q = Manager().Queue(maxsize=0)
        self.log_thread = LogThread(self)
        self.__MP = matplotlibDraw()

        self.initUI()

    def initUI(self):

        # label 显示图片
        self.__label = QLabel(self)
        self.__label.setStyleSheet("border: 2px solid red")
        self.__label.setScaledContents(True)

        # button 按钮
        self.crawl_btn = QPushButton('开始爬取', self)
        self.crawl_btn.clicked.connect(self.crawl_slot)

        # 布局
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.__label)
        self.v_layout.addWidget(self.crawl_btn)
        self.setLayout(self.v_layout)

        #显示窗口
        self.setGeometry(300, 300, 700, 600)
        self.setWindowTitle('结果')

    def showDraw(self, Img: ImageQt):
        """
        显示画图
        :param Img:
        :return:
        """
        self.__label.setPixmap(QPixmap(""))
        self.__label.setPixmap(QPixmap.fromImage(Img))

    def Draw(self, data: dict):
        img = self.__MP.Draw(data)
        if img:
            self.showDraw(img)

    def crawl_slot(self):
        """
        触发爬虫
        :return:
        """
        if self.crawl_btn.text() == '开始爬取':
            self.crawl_btn.setText('停止爬取')
            self.p = Process(target=crawl, args=(self.Q, self.__config))
            self.p.start()
            self.log_thread.start()
        else:
            self.crawl_btn.setText('开始爬取')
            self.p.terminate()
            self.log_thread.terminate()


class LogThread(QThread):
    def __init__(self, gui: QTAPP):
        super(LogThread, self).__init__()
        self.gui = gui

    def run(self):
        while True:
            if not self.gui.Q.empty():
                self.gui.Draw(self.gui.Q.get())
                # 睡眠10毫秒，否则太快会导致闪退或者显示乱码
                self.msleep(10)


if __name__ == '__main__':
    config = {
        'URL': 'http://localhost/', # 目标URL
        'Delay': 1, # 中间休息时间
        'matplotJudgment': 3# matplot规则
    }
    #创建应用程序和对象
    app = QApplication(sys.argv)
    ex = QTAPP(config)
    ex.show()
    sys.exit(app.exec_())