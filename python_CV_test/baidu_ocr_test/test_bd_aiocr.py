
# encoding:utf-8
import requests
import base64

def getsk():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=sr6Y4eoGyAUd7gjPHhZG1GlG&client_secret=NLAKthyMNZMwdQxF0clcESVQSDwAOHW1'
    response = requests.get(host)
    if response:
        print(response.json())

def sendimg():
    '''
    通用文字识别（高精度版）
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open('E:\\github\\testimg\\11.jpg', 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}
    access_token = '24.0573f577cab20c524f3be9a4d7da8871.2592000.1653484935.282335-26074288'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())

if __name__ == '__main__':
    sendimg()
