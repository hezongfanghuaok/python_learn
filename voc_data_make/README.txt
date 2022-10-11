checkxml.py  检查数据集 是否正常
voclist.py   用于划分voc数据集 训练和验证数据 生成test.txt train.txt trainval.txt val.txt
voc2012.py   用于制作tfrecord数据集合
gen_files.py 用于将voc数据集转换为yolo格式，并生成label文件夹，其下存放所有的voc转成的yolo格式的数据， 并生成2007_test.txt和2007_train.txt  生成的文件可以 用于darknet训练
voc_annotation.py 用于将voc数据集转换为yolo格式，并生成2007_test.txt和2007_train.txt    会将所有的yolo格式的标注数据直接写入2007_test.txt和2007_train.txt 每条记录的后面，生成数据集用于tf 平台的yolo训练
gen_anchors.py 聚类计算anchors值