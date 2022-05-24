import sys
import os
import argparse
import traceback
import cv2
import shutil
import random
import time


parser = argparse.ArgumentParser(description='Simple training script for training a RetinaNet network.')
parser.add_argument('--inputs', default='/home/work/datasets/VOC/voc', help='')
parser.add_argument('--outputs', default='/home/work/yangfg/tmp', help='')
args = parser.parse_args()


def main():

    for f in os.listdir(args.inputs):
        cap = cv2.VideoCapture(os.path.join(args.inputs, f))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(fps, width, height)

        out_dir = os.path.join(args.outputs, f[:-3])
        os.makedirs(out_dir, exist_ok=True)

        cnt = 0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret: break
            cnt += 1
            if cnt % 75 == 0:
                cv2.imwrite(os.path.join(out_dir, str(time.time()).replace('.', '') + '.jpg'), frame)
                cnt = 0
        cap.release()


if __name__ == '__main__':
    main()
