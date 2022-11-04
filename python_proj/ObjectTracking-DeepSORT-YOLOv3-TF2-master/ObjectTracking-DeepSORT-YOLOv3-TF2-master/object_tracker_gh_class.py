import datetime
import os
#os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
#os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import cv2
import numpy as np
import tensorflow as tf
from yolov3.utils import Load_Yolo_model, image_preprocess, postprocess_boxes, nms, draw_bbox, read_class_names
from yolov3.configs import *
import time
from yolo import YOLO
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from deep_sort import generate_detections as gdet
from PIL import Image
video_path = "bot.mp4"

def cap_video_img():
    if video_path:
        vid = cv2.VideoCapture(video_path)  # detect on video
    else:
        vid = cv2.VideoCapture(0)  # detect from webcam
    while True:
        _, frame0 = vid.read()
        # file_names = os.listdir('./img')
        # for name in file_names:
        try:

            original_frame = cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB)
            # 转变成Image
            frame = Image.fromarray(np.uint8(original_frame))
        except:
            break

        # 进行检测

class steel_tracker():
    def __init__(self):
        super().__init__()
        self.yolo = YOLO()
        max_cosine_distance = 0.7
        nn_budget = None
        # initialize deep sort object
        model_filename = 'model_data/mars-small128.pb'
        self.encoder = gdet.create_box_encoder(model_filename, batch_size=1)
        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
        self.tracker = Tracker(metric)
        self.CLASSES=YOLO_COCO_CLASSES


    #def Object_tracking(Yolo, video_path, output_path, input_size=416, show=False, CLASSES=YOLO_COCO_CLASSES, score_threshold=0.3, iou_threshold=0.45, rectangle_colors='', Track_only = []):
    def Object_tracking(self, frame0,Track_only = ["bottle"]):

        original_frame = cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB)
        # 转变成Image
        frame = Image.fromarray(np.uint8(original_frame))

        NUM_CLASS = read_class_names(self.CLASSES)
        key_list = list(NUM_CLASS.keys())
        val_list = list(NUM_CLASS.values())

        times, times_2 = [], []
        t1 = time.time()
        bboxes,yolodraw = self.yolo.detect_image(frame)
        t2 = time.time()

        boxes, scores, names = [], [], []
        for bbox in bboxes:
            if len(Track_only) !=0 and NUM_CLASS[int(bbox[5])] in Track_only or len(Track_only) == 0:
                boxes.append([bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]])
                scores.append(bbox[4])
                names.append(NUM_CLASS[int(bbox[5])])

        # Obtain all the detections for the given frame.
        boxes = np.array(boxes)
        names = np.array(names)
        scores = np.array(scores)
        features = np.array(self.encoder(original_frame, boxes))
        detections = [Detection(bbox, score, class_name, feature) for bbox, score, class_name, feature in zip(boxes, scores, names, features)]

        # Pass detections to the deepsort object and obtain the track information.
        self.tracker.predict()
        self.tracker.update(detections)

        # Obtain info from the tracks
        tracked_bboxes = []
        track_str =""
        for track in self.tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 5:
                continue
            bbox = track.to_tlbr() # Get the corrected/predicted bounding box
            class_name = track.get_class() #Get the class name of particular object
            tracking_id = track.track_id # Get the ID for the particular track
            index = key_list[val_list.index(class_name)] # Get predicted object index by object name
            tracked_bboxes.append(bbox.tolist() + [tracking_id, index]) # Structure data, that we could use it with our draw_bbox function

            coor = np.array(bbox[:4], dtype=np.int32)
            (x1, y1), (x2, y2) = (coor[0], coor[1]), (coor[2], coor[3])
            '''解析坐标          
            cv2.rectangle(original_frame, (x1, y1),  (x2, y2),(0, 0, 255),3 , -1)
            cv2.circle(original_frame, (np.int32(x1+(x2-x1)/2), np.int32(y1+(y2-y1)/2)), 3, (0, 0, 255), -1)
            cv2.imshow("dd", original_frame)
            cv2.waitKey(0)
            '''
            track_str+=str(tracking_id) + ":" + str((np.int32(x1 + (x2 - x1) / 2), np.int32(y1 + (y2 - y1) / 2)))+'!'

        # draw detection on frame
        cv2.line(original_frame,(400,10),(400,1200),(0, 0, 255))
        image = draw_bbox(original_frame, tracked_bboxes, CLASSES=self.CLASSES, tracking=True)
        t3 = time.time()
        times.append(t2-t1)
        times_2.append(t3-t1)

        times = times[-20:]
        times_2 = times_2[-20:]

        ms = sum(times)/len(times)*1000
        fps = 1000 / ms
        fps2 = 1000 / (sum(times_2)/len(times_2)*1000)

        image = cv2.putText(image, "Time: {:.1f} FPS".format(fps), (0, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
        return image,track_str

