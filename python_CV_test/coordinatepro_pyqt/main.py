import array
import os
import sys
from PyQt5.QtWidgets import QApplication, QDialog
import PointTransform
import untitled
import cv2
import numpy as np
import glob

class MainDialog(QDialog):

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)

        #self.ui = PointTransform.Ui_Dialog()
        self.ui=untitled.Ui_Form()
        self.ui.setupUi(self)

    def PlateShow(self):
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # 棋盘格模板规格
        w = 11
        h = 8
        # 世界坐标系中的棋盘格点,例如(0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)，去掉Z坐标，记为二维矩阵
        objp = np.zeros((w * h, 3), np.float32)
        objp[:, :2] = np.mgrid[0:w, 0:h].T.reshape(-1, 2)
        # 储存棋盘格角点的世界坐标和图像坐标对
        objpoints = []  # 在世界坐标系中的三维点
        imgpoints = []  # 在图像平面的二维点

        projectpoints = np.empty([9, 1, 2], dtype=np.float32)
        images = glob.glob(self.ui.textEdit_imgpath.toPlainText())
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 找到棋盘格角点
            ret, corners = cv2.findChessboardCorners(gray, (w, h), None)
            # 如果找到足够点对，将其存储起来  使用cornerSubPix函数  确定像素级角点  更加准确
            if ret == True:
                cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            objpoints.append(objp)
            imgpoints.append(corners)

            # cv写入yaml文件
            cv_file1 = cv2.FileStorage("chess.yaml", cv2.FILE_STORAGE_WRITE)
            # matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            print("write matrix\n", corners)
            cv_file1.write("corners", corners)
            cv_file1.release()
            # 将角点在图像上显示
            cv2.drawChessboardCorners(img, (w, h), corners, ret)
            cv2.imshow('findCorners', img)
            cv2.waitKey()
        cv2.destroyAllWindows()

    def my_fist_button_test(self):
        print("hellow")
        self.ui.mytest_label.setText("fuckckkckckck")
        # 标定
    def PointGet(self):
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # 棋盘格模板规格
        w = 11
        h = 8
        # 世界坐标系中的棋盘格点,例如(0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)，去掉Z坐标，记为二维矩阵
        objp = np.zeros((w * h, 3), np.float32)
        objp[:, :2] = np.mgrid[0:w, 0:h].T.reshape(-1, 2)
        # 储存棋盘格角点的世界坐标和图像坐标对
        objpoints = []  # 在世界坐标系中的三维点
        imgpoints = []  # 在图像平面的二维点

        projectpoints = np.empty([9, 1, 2], dtype=np.float32)
        images = glob.glob(self.ui.textEdit_imgpath.toPlainText())
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 找到棋盘格角点
            ret, corners = cv2.findChessboardCorners(gray, (w, h), None)
            # 如果找到足够点对，将其存储起来  使用cornerSubPix函数  确定像素级角点  更加准确
            if ret == True:
                cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            objpoints.append(objp)
            imgpoints.append(corners)
            # 棋盘格第一行

            projectpoints[0] = corners[(int(self.ui.textEdit_row1inplate.toPlainText())-1) * 11 + (int(self.ui.textEdit_row1point1.toPlainText())-1)]
            projectpoints[1] = corners[(int(self.ui.textEdit_row1inplate.toPlainText())-1) * 11 + (int(self.ui.textEdit_row1point2.toPlainText())-1)]
            projectpoints[2] = corners[(int(self.ui.textEdit_row1inplate.toPlainText())-1) * 11 + (int(self.ui.textEdit_row1point3.toPlainText())-1)]
            # 棋盘格第5行
            projectpoints[3] = corners[(int(self.ui.textEdit_row2inplate.toPlainText())-1) * 11 + (int(self.ui.textEdit_row2point1.toPlainText())-1)]
            projectpoints[4] = corners[(int(self.ui.textEdit_row2inplate.toPlainText())-1) * 11 + (int(self.ui.textEdit_row2point2.toPlainText())-1)]
            projectpoints[5] = corners[(int(self.ui.textEdit_row2inplate.toPlainText())-1) * 11 + (int(self.ui.textEdit_row2point3.toPlainText())-1)]

            # 棋盘格第8行
            projectpoints[6] = corners[(int(self.ui.textEdit_row3inplate.toPlainText())-1) * 11 + (int(self.ui.textEdit_row3point1.toPlainText())-1)]
            projectpoints[7] = corners[(int(self.ui.textEdit_row3inplate.toPlainText())-1) * 11 + (int(self.ui.textEdit_row3point2.toPlainText())-1)]
            projectpoints[8] = corners[(int(self.ui.textEdit_row3inplate.toPlainText())-1) * 11 + (int(self.ui.textEdit_row3point3.toPlainText())-1)]

            # cv写入yaml文件
            cv_file1 = cv2.FileStorage("chess.yaml", cv2.FILE_STORAGE_WRITE)
            # matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            print("write matrix\n", corners)
            cv_file1.write("corners", corners)
            cv_file1.release()
            # 九点标定数据写入yaml文件
            cv_file2 = cv2.FileStorage("project.yaml", cv2.FILE_STORAGE_WRITE)
            projectpoints = projectpoints.reshape(9, 2)
            print("projectpoints\n", projectpoints)
            cv_file2.write("projectpoints", projectpoints)
            cv_file2.release()
            # 将角点在图像上显示
            cv2.drawChessboardCorners(img, (w, h), corners, ret)
            # cv2.imshow('findCorners', img)
            cv2.waitKey()
        cv2.destroyAllWindows()

        # 标定

    def Transform(self):
        cv_file = cv2.FileStorage("project.yaml", cv2.FILE_STORAGE_READ)
        matrix1 = cv_file.getNode("projectpoints").mat()

        matrix2 = []
        data = open('TXTtest', 'w')
        # data = str(self.ui.textEdit_imgpath_2.toPlainText())  # 将字符串读入data
        data.write(self.ui.textEdit_imgpath_2.toPlainText())
        data = open('TXTtest', 'r')

        for line in data:
            numbers = line.split()  # 将数据分隔
            numbers_float = list(map(float, numbers))  # 转化为浮点数
            matrix2.append(numbers_float)
        matrix2 = np.array(matrix2)

        mat2dtest, inlins = cv2.estimateAffine2D(matrix1, matrix2)

        # cv写入yaml文件
        cv_file1 = cv2.FileStorage("mat2dtest.yaml", cv2.FILE_STORAGE_WRITE)
        print("write matrix\n", mat2dtest)
        cv_file1.write("mat2d", mat2dtest)
        cv_file1.release()


myapp = QApplication(sys.argv)

myDlg = MainDialog()

myDlg.show()

sys.exit(myapp.exec_())