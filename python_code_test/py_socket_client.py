import socket
import sys

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = '127.0.0.1'

# 设置端口号
port = 60000

# 连接服务，指定主机和端口
s.connect((host, port))
data="fuck test"+ "\r\n"
# 接收小于 1024 字节的数据
msg = s.send(data.encode('utf-8'))

s.close()

print (data)