from cv2 import cv2
import numpy as np

p=np.array((2,3)).reshape(-1,1,2)
p=np.zeros((2,3)).reshape(-1,2,3)
print(p)
ph=cv2.convertPointsToHomogeneous(p) 

print(ph)