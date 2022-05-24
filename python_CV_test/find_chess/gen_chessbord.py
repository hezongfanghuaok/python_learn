from cv2 import cv2
import numpy as np

checker_img = np.zeros((1350,1800))
block_width = 150
white_block = np.full((block_width,block_width),255)
for row in range(9):
    for col in range(12):
        if (row+col)%2==0:
            row_begin = row*block_width
            row_end = row_begin+block_width
            col_begin = col*block_width
            col_end = col_begin+block_width
            checker_img[row_begin:row_end,col_begin:col_end] = white_block
cv2.imwrite("checker_board.jpg",checker_img)
cv2.imshow("checker_board",checker_img)
cv2.waitKey(0)