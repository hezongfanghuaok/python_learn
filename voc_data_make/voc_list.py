# -*- coding：utf-8 -*-
# -*- python3.5 根据比例生成训练集和测试集合 在imagesets中生成几个text文件
import os
import random

trainval_percent = 0.2  # 可以自己设置
train_percent = 0.8  # 可以自己设置

xmlfilepath = './VOCdevkit/VOC2007/Annotations'  # 地址填自己的
txtsavepath = './VOCdevkit/VOC2007/ImageSets/Main'
total_xml = os.listdir(xmlfilepath)

num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

ftrainval = open(txtsavepath + '/trainval.txt', 'w')
ftest = open(txtsavepath + '/test.txt', 'w')
ftrain = open(txtsavepath + '/train.txt', 'w')
fval = open(txtsavepath + '/val.txt', 'w')

for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()
print('Well finshed')
