import datetime
import sys
import cv2
import math
from PIL import Image
import pymysql
import  re
from track_UI.config_sql_item import sql_executor
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import queue
import numpy as np
from object_tracker_gh_class import steel_tracker
import time
# 软件的配置文件读取类
from track_UI.track_ui import Ui_MainWindow
import yaml
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(CURRENT_PATH, '..'))
CONFIG_NAME = 'config.yaml'
video_path = "./bot.mp4"

class Thread_1(QThread):  # 线程1
    def __init__(self):
        super().__init__()
        self.t1=steel_tracker()
        self.getaimqueu=queue.Queue(50)
        self.getaimlist=[]
    #通过定义信号  更新界面label图片和listview
    update_data = pyqtSignal(QPixmap)
    update_datalistv = pyqtSignal(str)
    def run(self):
        if video_path:
            vid = cv2.VideoCapture(video_path)  # detect on video
        else:
            vid = cv2.VideoCapture(0)  # detect from webcam
        while True:
            _, frame0 = vid.read()
            try:
                #time.sleep(0.2)
                img,track_str = self.t1.Object_tracking(frame0)
                res = cv2.resize(img, (int(600), int(800)), interpolation=cv2.INTER_CUBIC)  # 用cv2.resize设置图片大小
                img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
                _image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
                jpg_out = QPixmap(_image)
                self.update_data.emit(QPixmap(_image))
                #sqltxt="DELETE FROM LongWidth WHERE time >= '%s'and time <= '%s'" % (self.start, self.end)
                if track_str:
                    #数据库记录所有跟踪目标
                    #sqltxt = "insert into sqlTest (name) values ('%s')" % (track_str)
                    #sql_executor.execute(sqltxt)
                    print(track_str)
                    alltrack=track_str.split('!')
                    for onetrack in alltrack:
                        if onetrack:
                            oneid = onetrack.split(':')
                            id=oneid[0]
                            p1 = re.compile(r'[(](.*?)[)]', re.S)  # 最小匹配
                            xpos=re.findall(p1, oneid[1])[0].split(',')[0]
                            if int(xpos)>400:
                                if id not in self.getaimlist:
                                    messagetxt = "%s:aim object %s into the place" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), onetrack)
                                    self.update_datalistv.emit(messagetxt)
                                if len(self.getaimlist)<=50:
                                    self.getaimlist.append(id)
                                else:
                                    self.getaimlist.pop(50)
                                    self.getaimlist.append(id)
                                    # 数据库记录所有过线目标
                                    # sqltxt = "insert into aim_arrival (arrival_time,local) values ('%s','%s')" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),onetrack)
                                    # sql_executor.execute(sqltxt)
                                    #[item for item in enumerate(self.getaimlist) if item.is_confirmed()]
            except:
                break

class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.list1 = []
        self.model = QStringListModel()
        self.setupUi(self)
        self.index()


    def index(self):
        self.pushButton.clicked.connect(self.slotStart)

    #更新player_label
    def Updateimg(self, jpg_out):
        self.player_label.setPixmap(jpg_out)
        self.player_label.repaint()

    def Updatelistview(self,listmsg):
        self.list1.append(listmsg)
        self.model.setStringList(self.list1)
        self.message_listv.setModel(self.model)

    def slotStart(self):
        self.thread_1 = Thread_1()  # 创建线程
        #连接子线程与更新程序  Updateimg(self, jpg_out)-->self.thread_1.update_data.connect(self.Updateimg)<--update_data = pyqtSignal(QPixmap)
        self.thread_1.update_data.connect(self.Updateimg)
        self.thread_1.update_datalistv.connect(self.Updatelistview)
        self.thread_1.start()
        #self.timer_camera.start(100)
        #self.timer_camera.timeout.connect(self.showimg)

'''
    def showimg(self):
        file_names = os.listdir('./img')
        for name in file_names:
            time.sleep(1)
            img = self.y1.testimg("./img/"+name)
            res = cv2.resize(img, (int(937), int(256)), interpolation=cv2.INTER_CUBIC)  # 用cv2.resize设置图片大小
            img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
            _image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
            jpg_out = QPixmap(_image)
            print("steel.jpg")
            self.player_label.setPixmap(jpg_out)
            self.player_label.repaint()

'''



def run():
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    QApplication.processEvents()
    window.setFixedSize(1000,800 )
    window.show()
    sys.exit(app.exec_())
