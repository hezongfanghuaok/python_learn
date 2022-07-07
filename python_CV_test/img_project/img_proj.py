import cv2
import numpy as np
import glob

#两组2d坐标转换  得到转换矩阵
matrix1 = np.array([[1034.7388916 ,  684.09613037], [772.74993896,   689.4161377], [509.26437378,   693.92810059 ],[1030.6295166 ,   527.36096191], [769.69049072,   531.95776367], [506.98348999,   536.55010986],[1024.79992676,   319.84289551], [765.5489502 ,   323.61978149], [504.41970825,   328.69494629]])
matrix2 = np.array([[612.867,-65.59], [862.01,-69.66], [1113.16,-72.96],[614.92,83.25], [ 864.25,79.43], [1114.93,75.06],[ 618.15,283.03], [867.80,277.88], [1117.65,273.89]])
mat2dtest,inlins=cv2.estimateAffine2D(matrix1,matrix2)
cv2.calibrateHandEye()
# cv写入yaml文件
cv_file1 = cv2.FileStorage("mat2dtest.yaml", cv2.FILE_STORAGE_WRITE)
print("write matrix\n", mat2dtest)
cv_file1.write("mat2d", mat2dtest)
cv_file1.release()

cv2.destroyAllWindows()

# 标定