# coding: utf-8
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math

def test():

    #生成x数据
    X = np.random.randint(25, 50, (25, 2))
    # 生成y数据
    Y = np.random.randint(60, 85, (25, 2))
    Z = np.vstack((X, Y))
    Z = np.float32(Z)
    #第一个参数：criteria满足终止条件
    #cv.TERM_CRITERIA_EPS - 达到精度epsilon就停止迭
    #cv.TERM_CRITERIA_MAX_ITER - 达到最大迭代次数max_iter就停止迭代
    # cv.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER - 满足上述任何条件停止迭代第二个参数
    # 第二个参数 10：max_iter - 最大迭代次数
    # 第三个参数 1.0：  epsilon - 要求的精度
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    #1. samples   np.float32类型的训练数据
    #2. nclusters(K) 需要分类的数目
    #3. critria 满足终止的条件，满足这个条件，就停止迭代
    #4. attempts:  使用flag指定的算法初始执行算法的次数，估计是通过多次初始化得到一个准确值。
    #5. flags : 指定初始的中心点的方式，通常又两种方式，cv.KMEANS_PP_CENTERS和cv.KMEANS_RANDOM_CENTERS
    #返回的参数为
    #1.compactness : 每个点到其相应中心的平方距离之和
    #2. labels :  标签数组，其中每个元素标记为0、1、2等等
    #3. centers :  各组集群的中心
    ret, label, center = cv.kmeans(Z, 2, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
    A = Z[label.ravel() == 0]
    B = Z[label.ravel() == 1]
    plt.scatter(A[:, 0], A[:, 1])
    plt.scatter(B[:, 0], B[:, 1], c='r')
    plt.scatter(center[:, 0], center[:, 1], s=80, c='y', marker='s')
    plt.xlabel('Height'), plt.ylabel('Weight')
    plt.show()

def testforone():

    yamlpath = "./test.yaml"
    cv_file = cv.FileStorage(yamlpath, cv.FILE_STORAGE_READ)  # 实例化一个 FileStorage
    mat = cv_file.getNode("xypoints").mat()
    cv_file.release()
    #生成x数据
    X = mat


    Z = np.float32(X)
    meanvalue=Z.mean(axis=0)
    #meanvalue=np.mean(Z)
    #第一个参数：criteria满足终止条件
    #cv.TERM_CRITERIA_EPS - 达到精度epsilon就停止迭
    #cv.TERM_CRITERIA_MAX_ITER - 达到最大迭代次数max_iter就停止迭代
    # cv.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER - 满足上述任何条件停止迭代第二个参数
    # 第二个参数 10：max_iter - 最大迭代次数
    # 第三个参数 1.0：  epsilon - 要求的精度
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    #1. samples   np.float32类型的训练数据
    #2. nclusters(K) 需要分类的数目
    #3. critria 满足终止的条件，满足这个条件，就停止迭代
    #4. attempts:  使用flag指定的算法初始执行算法的次数，估计是通过多次初始化得到一个准确值。
    #5. flags : 指定初始的中心点的方式，通常又两种方式，cv.KMEANS_PP_CENTERS和cv.KMEANS_RANDOM_CENTERS
    #返回的参数为
    #1.compactness : 每个点到其相应中心的平方距离之和
    #2. labels :  标签数组，其中每个元素标记为0、1、2等等
    #3. centers :  各组集群的中心
    ret, label, center = cv.kmeans(Z, 2, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
    A = Z[label.ravel() == 0]
    B = Z[label.ravel() == 1]
    leftcenter=np.array([center[0][0]-20,center[0][1]])
    rightcenter=np.array([[center[0][0]+5,center[0][1]]])
    dis_point=dict()
    sort_point = dict()
    for i in range(len(A)):
       dis=getdis(A[i],leftcenter)
       dis_point.update({dis:A[i]})
    sort_point=sorted(dis_point.items(),key=lambda x:x[0])

    


    #B = Z[label.ravel() == 1]
    plt.scatter(A[:, 0], A[:, 1])
    plt.scatter(B[:, 0], B[:, 1], c='r')
    plt.scatter(center[:, 0], center[:, 1], s=80, c='y', marker='s')


    plt.xlabel('Height'), plt.ylabel('Weight')
    plt.show()


def getdis(point1,point2):
    dis=math.sqrt(math.pow(point1[0]-point2[0],2)+math.pow(point1[1]-point2[1],2))
    return dis

if __name__ == '__main__':
    testforone()
