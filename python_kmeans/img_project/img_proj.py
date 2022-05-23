import cv2
import numpy as np
import glob


#cv读取yaml文件
yamlpath = "./chess.yaml"
cv_file = cv2.FileStorage(yamlpath, cv2.FILE_STORAGE_READ) # 实例化一个 FileStorage
mat = cv_file.getNode("corners").mat()
cv_file.release()

# 找棋盘格角点
# 阈值
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# 棋盘格模板规格
w = 9
h = 6
# 世界坐标系中的棋盘格点,例如(0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)，去掉Z坐标，记为二维矩阵
objp = np.zeros((w * h, 3), np.float32)
objp[:, :2] = np.mgrid[0:w, 0:h].T.reshape(-1, 2)
# 储存棋盘格角点的世界坐标和图像坐标对
objpoints = []  # 在世界坐标系中的三维点
imgpoints = []  # 在图像平面的二维点

images = glob.glob('../testimg/*.jpg')
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
    print("write matrix\n", corners)
    cv_file1.write("corners", corners)
    cv_file1.release()

    # 将角点在图像上显示
    #cv2.drawChessboardCorners(img, (w, h), corners, ret)
    #cv2.imshow('findCorners', img)
    #cv2.waitKey()
    
mat2d,inlins=cv2.estimateAffine2D(corners,corners)
# cv写入yaml文件
cv_file1 = cv2.FileStorage("mat2d.yaml", cv2.FILE_STORAGE_WRITE)
print("write matrix\n", mat2d)
cv_file1.write("mat2d", mat2d)
cv_file1.release()


matrix1 = np.array([[1, 3], [49, 4], [7.5, 8],[1, 3], [3, 5], [7, 8],[1, 2], [2, 5], [98, 8]],'2f')
matrix2 = np.array([[1, 2], [4, 5], [7, 8],[1, 29], [4, 59], [37, 8],[1, 32], [4, 5], [37, 8]])

mat2dtest,inlins=cv2.estimateAffine2D(matrix1,matrix2)
# cv写入yaml文件
cv_file1 = cv2.FileStorage("mat2dtest.yaml", cv2.FILE_STORAGE_WRITE)
print("write matrix\n", mat2dtest)
cv_file1.write("mat2d", mat2dtest)
cv_file1.release()

cv2.destroyAllWindows()

# 标定