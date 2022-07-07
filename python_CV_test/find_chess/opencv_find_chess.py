import cv2
import numpy as np
import glob

# 找棋盘格角点
# 阈值
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

images = glob.glob('../testimg/1.bmp')
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
    #matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print("write matrix\n", corners)
    cv_file1.write("corners", corners)
   # cv_file1.release()

    # 将角点在图像上显示
    cv2.drawChessboardCorners(img, (w, h), corners, ret)
    cv2.imshow('findCorners', img)
    cv2.waitKey()
cv2.destroyAllWindows()

centpoints = []
cornerlen=len(corners)

a=int(11/10)
for i in range(len(corners)-18):
    onecenter=corners[int(i/10)+i]
    anpoint=corners[int(i/10+i)+12]
    x=onecenter[0][0]+(anpoint[0][0]-onecenter[0][0])/2
    y = onecenter[0][1] + (anpoint[0][1]  - onecenter[0][1] ) / 2
    centpoints.append([x,y])


#1  5  9
#21 25 29
#41 45 49   int(i/3)*20+(4*(i%3)-3)


for i in range(8):
    for j in range(11-1):
        onecenter=corners[j*i+j]
        anpoint=corners[(j*i+j)+12]
        centpoints.append(onecenter)
# 标定