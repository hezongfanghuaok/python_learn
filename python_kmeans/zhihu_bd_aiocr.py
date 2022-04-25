import sys
import os
import glob
from os import path
from aip import AipOcr
from PIL import Image


# mupic2text mu可以对文件路径下所有的文件转化，pic2text 图片转text
def mupic2text(picturefile, outputfile):
    filename = glob.glob(picturefile)
    APP_ID = '26074288'  # 写入申请的ID
    API_KEY = 'sr6Y4eoGyAUd7gjPHhZG1GlG'
    SECRECT_KEY = 'NLAKthyMNZMwdQxF0clcESVQSDwAOHW1'
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
    for fname in filename:
        pic = open(fname, 'rb')
        img = pic.read()
        print("正在识别图片：" + str(fname))
        ##        resp = client.basicGeneral(img)   # 普通文字识别，每天 50000 次免费
        resp = client.basicAccurate(img)  # 高精度识别，每天 800 次免费
        print(str(fname) + "识别成功！")
        pic.close();

        with open(outputfile, 'a+') as fo:
            for text in resp.get('words_result'):
                fo.writelines(text.get('words') + '\n')
            fo.writelines('\n' * 2)


picturefile = "E:\\github\\testimg\\ocrtest.jpg"  # 图片路径
outputfile = 'pictotext.txt'  # 转换的后的文件名，路径在python脚本所在的路径下
if path.exists(outputfile):
    os.remove(outputfile)
mupic2text(picturefile, outputfile)