import yaml
import cv2
import sys
import numpy as np
with open("config.yaml") as f:
    config = yaml.safe_load(f.read())
    if config is None:
        sys.exit(1)
client = config.get('database')
host = client['host']
user = client['user']
passwd = client['passwd']
db = client['db']


#cv读取yaml文件
yamlpath = "./test3.yaml"
cv_file = cv2.FileStorage(yamlpath, cv2.FILE_STORAGE_READ) # 实例化一个 FileStorage
mat = cv_file.getNode("my_matrix").mat()
cv_file.release()

#cv写入yaml文件
cv_file1 = cv2.FileStorage("test3.yaml", cv2.FILE_STORAGE_WRITE)
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("write matrix\n", matrix)
cv_file1.write("my_matrix", matrix)
cv_file1.release()

print("ok")