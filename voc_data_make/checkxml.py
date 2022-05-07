#因下载的数据集中有字段空缺，因此通过该脚验证是否含有size键 没有时记录相关文件名称 并删除相关文件
import time
import os
import hashlib

import re
import string
path="./23img/"
from absl import app, flags, logging
from absl.flags import FLAGS

import lxml.etree
import tqdm

flags.DEFINE_string('data_dir', './VOC2007/',
                    'path to raw PASCAL VOC dataset')
flags.DEFINE_enum('split', 'val', [
                  'train', 'val'], 'specify train or val spit')
flags.DEFINE_string('output_file', './voc_2_tf/mask_val.tfrecord', 'outpot dataset')
flags.DEFINE_string('classes', './vocfuck.names', 'classes file')



def parse_xml(xml):
    if not len(xml):
        return {xml.tag: xml.text}
    result = {}
    for child in xml:
        child_result = parse_xml(child)
        if child.tag != 'object':
            result[child.tag] = child_result[child.tag]
        else:
            if child.tag not in result:
                result[child.tag] = []
            result[child.tag].append(child_result[child.tag])
    return {xml.tag: result}

ftrainval = open('./badxml.txt', 'w')
file_names = os.listdir('./vOC2007/Annotations')
def main(_argv):
    for name in file_names:
        annotation_xml = lxml.etree.fromstring(open('./vOC2007/Annotations/'+name).read())
        annotation = parse_xml(annotation_xml)['annotation']
        if 'size' not in annotation :
            ftrainval.write(name)
            ftrainval.write('\n')
            #os.remove('./vOC2007/Annotations/'+name)
    ftrainval.close()



    ftrainval.close()
    logging.info("Done")


if __name__ == '__main__':
    app.run(main)
