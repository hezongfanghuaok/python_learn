# -*- coding：utf-8 -*-
# -*- python3.5 根据比例生成训练集和测试集合 在imagesets中生成几个text文件
import os
import random

trainval_percent =0.9   # 训练验证集占整个数据集的比重（划分训练集和测试验证集）
train_percent =0.8   # 训练集占整个训练验证集的比重（划分训练集和验证集）

xmlfilepath = './VOCdevkit/VOC2007/Annotations'  # 地址填自己的
txtsavepath = './VOCdevkit/VOC2007/ImageSets/Main'
total_xml = os.listdir(xmlfilepath)

num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(num * train_percent)
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
