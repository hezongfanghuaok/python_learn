import numpy as np
import re
from scipy.optimize import linear_sum_assignment

def linear_sum():
    cost_matrix = np.array([
        [15, 40, 45],
        [20, 60, 35],
        [20, 40, 25]
    ])

    matches = linear_sum_assignment(cost_matrix)
    print('scipy API result:\n', matches)

"""Outputs
sklearn API result:
 [[0 1]
  [1 0]
  [2 2]]
scipy API result:
 (array([0, 1, 2], dtype=int64), array([1, 0, 2], dtype=int64))
"""

def testlistfor():
    a=[x for x in range(5) if x%2 ==0 ]  # [0, 1, 2, 3, 4]
    return a
def testmtricmax():
    maxnum=20
    a=np.array([[1,2,32],[3,5,6],[34,54,3]])
    a[a>maxnum]=maxnum+2
    return a
def argmin_min():
    lst1 = [1, 100, 56, 78, 0]
    lst2 = [[100, 4, 5], [3, 5, 7], [5, 0, 6]]
    print("lst列表中的最小值是:")
    print(np.min(lst1))
    print("lst1列表中最小值的索引是：")
    print(np.argmin(lst1))
    print("lst2列表中最小值的索引是：")
    print(np.argmin(lst2))
    print("lst2列表中最值，按照轴0方向：")
    print(lst2)
    print(np.min(lst2,axis=0))
def findkuohao():
    string = 'abe(ac)ad)'
    p1 = re.compile(r'[(](.*?)[)]', re.S)  # 最小匹配
    p2 = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配
    print(re.findall(p1, string))
    print(re.findall(p2, string))

def main():
    findkuohao()

if __name__ == '__main__':
    main()