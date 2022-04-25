import sys
import cv2
import math

import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from predict import yolotest
import time
# 软件的配置文件读取类
from client.Ui_qt_gui import Ui_MainWindow
import yaml
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(CURRENT_PATH, '..'))
CONFIG_NAME = 'config.yaml'

class Thread_1(QThread):  # 线程1
    def __init__(self):
        super().__init__()
        self.y1=yolotest()
    #更新界面label图片  通过定义信号
    update_data = pyqtSignal(QPixmap)
    def run(self):
        while True:
            file_names = os.listdir('./img')
            for name in file_names:
                time.sleep(1)
                img = self.y1.testimg("./img/" + name)
                #img=cv2.imread("./img/" + name)
                res = cv2.resize(img, (int(937), int(256)), interpolation=cv2.INTER_CUBIC)  # 用cv2.resize设置图片大小
                img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
                _image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                                QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
                jpg_out = QPixmap(_image)
                print(name)
                self.update_data.emit(QPixmap(_image))
                #self.player_label.setPixmap(jpg_out)
                #self.player_label.repaint()



class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.index()
        self.timer_camera = QTimer()

    def index(self):

        file_path = os.path.join(CURRENT_PATH, CONFIG_NAME)
        with open(file_path) as f:
            config = yaml.safe_load(f.read())
            if config is None:
                sys.exit(1)
        self.client = config.get('database')
        self.host = self.client['host']
        self.user = self.client['user']
        self.passwd = self.client['passwd']
        self.db = self.client['db']

        self.labelstyle()
        self.createtabledata()
        self.tabWidget.currentChanged['int'].connect(self.tebleclick)
        self.sousuo.clicked.connect(self.searchtime)
        self.shanchu.clicked.connect(self.delete)
        self.pushButton.clicked.connect(self.previous)
        self.pushButton_2.clicked.connect(self.next)
        self.pushButton_3.clicked.connect(self.slotStart)
    #更新player_label
    def Updateimg(self, jpg_out):
        self.player_label.setPixmap(jpg_out)
        self.player_label.repaint()
    def slotStart(self):
        self.thread_1 = Thread_1()  # 创建线程
        #连接子线程与更新程序  Updateimg(self, jpg_out)-->self.thread_1.update_data.connect(self.Updateimg)<--update_data = pyqtSignal(QPixmap)
        self.thread_1.update_data.connect(self.Updateimg)
        self.thread_1.start()
        #self.timer_camera.start(100)
        #self.timer_camera.timeout.connect(self.showimg)

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




    def labelstyle(self):
        self.title.setAlignment(Qt.AlignCenter)
        self.signal_1.setStyleSheet(
            "QLabel{min-width: 20px; min-height: 20px;max-width:20px; max-height: 20px;border-radius: 10px;  "
            "border:1px solid red;background:red}")
        self.signal_text1.setText("异常")
        self.signal_2.setStyleSheet(
            "QLabel{min-width: 20px; min-height: 20px;max-width:20px; max-height: 20px;border-radius: 10px;  "
            "border:1px solid yellow;background:yellow}")
        self.signal_text2.setText("连接中")

    def tebleclick(self, index):
        if (index == 1):
            self.tabledata()
            self.start = ""
            self.end = ""
            self.tableplay()

    def tableplay(self):
        self.search()
        self.nowpage = 1
        self.page = 0
        # self.shuzi初始值必须与self.showdata相同
        self.shuzi = 50
        self.showdata = 50

        self.tablebox()
        self.allpage = math.ceil(len(self.data) / self.showdata)
        self.pagetext.setText("第" + str(self.nowpage) + "页/共" +
                              str(self.allpage) + "页  共" + str(len(self.data)) + "条数据")

    # 设置日历控件
    def search(self):
        # 设置开始时间
        self.time_start.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.time_start.setMinimumDate(QDate.currentDate().addDays(-365))
        self.time_start.setMaximumDate(QDate.currentDate().addDays(0))
        # # 设置日历控件允许弹出
        self.time_start.setCalendarPopup(True)
        # 当日期时间改变时触发槽函数
        self.time_start.dateTimeChanged.connect(self.onDateTimestart)
        # 设置结束时间
        self.time_end.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.time_end.setMinimumDate(QDate.currentDate().addDays(-365))
        self.time_end.setMaximumDate(QDate.currentDate().addDays(0))
        # 设置日历控件允许弹出
        self.time_end.setCalendarPopup(True)
        self.time_end.dateTimeChanged.connect(self.onDateTimeend)

    # 开始时间的回调函数
    def onDateTimestart(self, dateTime):
        self.start = dateTime.toString("yyyy-MM-dd hh:mm:ss")

    # 结束时间的回调函数
    def onDateTimeend(self, dateTime):
        self.end = dateTime.toString("yyyy-MM-dd hh:mm:ss")

    # 点击搜索按钮
    def searchtime(self):
        if self.start == "":
            timestart = QDateTime.currentDateTime()
            self.start = timestart.toString("yyyy-MM-dd hh:mm:ss")
        if self.end == "":
            timeend = QDateTime.currentDateTime()
            self.end = timeend.toString("yyyy-MM-dd hh:mm:ss")
        if self.start >= self.end:
            QMessageBox.information(
                self, "提示", "开始时间不可大于或等于结束时间", QMessageBox.Yes)
        else:
            self.model.clear()
            self.page = 0
            self.tabledata_1()
            self.tableplay()

    # 点击删除按钮
    def delete(self):
        if self.start == "":
            timestart = QDateTime.currentDateTime()
            self.start = timestart.toString("yyyy-MM-dd hh:mm:ss")
        if self.end == "":
            timeend = QDateTime.currentDateTime()
            self.end = timeend.toString("yyyy-MM-dd hh:mm:ss")
        if self.start >= self.end:
            QMessageBox.information(
                self, "提示", "开始时间不可大于或等于结束时间", QMessageBox.Yes)
        else:
            self.delbutton = QMessageBox.warning(
                self, "提示", "确定删除"+self.start+"至"+self.end+"的数据？",  QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
            if self.delbutton == 16384:
                self.deletedata()

    def deletedata(self):
        # 打开数据库连接
        conn = pymysql.connect(
            host=self.host, user=self.user, passwd=self.passwd, db=self.db)
        # 游标对象
        cur = conn.cursor()
        # 删除的sql语句
        sql = "DELETE FROM LongWidth WHERE time >= '%s'and time <= '%s'" % (
            self.start, self.end)
        # 注入sql语句
        cur.execute(sql)
        try:
            cur.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        conn.close()

        self.tabledata()
        self.tableplay()
        self.tishi = QMessageBox.warning(self, "提示", "删除成功",  QMessageBox.Yes)

    def createtabledata(self):
        # 判断是否有保存数据的表，如果没有就新建一个
        conn = pymysql.connect(
            host=self.host, user=self.user, passwd=self.passwd, db=self.db)
        cur = conn.cursor()
        sql = "CREATE TABLE IF NOT EXISTS `LongWidth` (\
                `time` timestamp(0) NOT NULL,\
                `width` char(255) default NULL, \
                `height` char(255) default NULL, \
                PRIMARY KEY (`time`))ENGINE=InnoDB DEFAULT CHARSET=utf8;"
        try:
            cur.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        conn.close()

    # 初始调用
    def tabledata(self):
        # 打开数据库连接
        conn = pymysql.connect(
            host=self.host, user=self.user, passwd=self.passwd, db=self.db)
        # 游标对象
        cur = conn.cursor()
        # 查询的sql语句
        sql = "SELECT * FROM LongWidth"
        cur.execute(sql)
        self.data = cur.fetchall()[::-1]
        conn.close()

    # 查询调用
    def tabledata_1(self):
        # 打开数据库连接
        conn = pymysql.connect(
            host=self.host, user=self.user, passwd=self.passwd, db=self.db)
        # 游标对象
        cur = conn.cursor()
        # 查询的sql语句
        sql = "SELECT * FROM LongWidth where time >= %s and time < %s"
        # 注入sql语句
        cur.execute(sql, (self.start, self.end))
        self.data = cur.fetchall()[::-1]
        conn.close()

    def tablebox(self):
        self.model = QStandardItemModel(self.showdata, 3)
        # 设置表头
        self.model.setHorizontalHeaderLabels(['检测时间', '钢板宽度', '钢板长度'])
        # 列宽自适应充满表格
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 关联QTableView控件和Model
        self.tableView.setModel(self.model)
        # 表格不可编辑
        self.tableView.setEditTriggers(QTableView.NoEditTriggers)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 判断是否在第一页或最后一页
        if len(self.data) < self.showdata:
            self.xunhuan = len(self.data)
        elif self.shuzi < self.showdata:
            self.xunhuan = self.shuzi
        else:
            self.xunhuan = self.showdata
        # 在表格中添加数据
        for i in range(0, self.xunhuan):
            self.t = i + self.page
            item11 = QStandardItem(
                self.data[self.t][0].strftime("%Y-%m-%d %H:%M:%S"))
            item12 = QStandardItem(self.data[self.t][1])
            item13 = QStandardItem(self.data[self.t][2])
            self.model.setItem(i, 0, item11)
            self.model.setItem(i, 1, item12)
            self.model.setItem(i, 2, item13)

    # 点击上一页
    def previous(self):
        self.shuzi = self.showdata
        if self.page >= self.showdata:
            self.nowpage = self.nowpage - 1
            self.page = self.page - self.showdata
            self.tablebox()
            self.pagetext.setText("第" + str(self.nowpage) + "页/共" +
                                  str(self.allpage) + "页  共" + str(len(self.data)) + "条数据")
        else:
            QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)

    # 点击下一页
    def next(self):
        if self.nowpage + 1 > self.allpage:
            QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
        else:
            self.model.clear()
            self.nowpage = self.nowpage + 1
            self.page = self.page + self.showdata
            self.shuzi = len(self.data) - self.t - 1
            self.tablebox()
            self.pagetext.setText("第" + str(self.nowpage) + "页/共" +
                                  str(self.allpage) + "页  共" + str(len(self.data)) + "条数据")


def run():
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    QApplication.processEvents()
    window.setFixedSize(1040, 985)
    window.show()
    sys.exit(app.exec_())
