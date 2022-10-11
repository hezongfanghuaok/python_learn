import cv2
import numpy as np
import yaml

def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
 
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
 
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
 
	# return the ordered coordinates
	return rect


def four_point_transform(image, pts,rect1):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
 
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
 
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))

	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")

	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect1, dst)
	size=image.shape[:2]
	warped = cv2.warpPerspective(image, M,(maxWidth, maxHeight))

	# return the warped image
	return warped

if __name__ == '__main__':



	#大图
	#rect = np.array([(1275.8,161.0), (2709.2, 401.7), (2579.5, 818.4), (833.2, 461.03)], dtype="float32")
	#dst = np.array([(500, 200), (2000, 200), (2000, 700), (500, 700)], dtype="float32")
	#中图
	rect = np.array([(636.1, 79.2), (1352.3, 200.9), (1287.8, 394.2), (417.6, 231.8)], dtype="float32")
	dst = np.array([(200, 100), (1200, 100), (1200, 400), (200, 400)], dtype="float32")
	#img=cv2.imread("../video/1432_872_fps8_4min_img/162347386089601.jpg")
	img= cv2.imread("../video/2864_1744_fps2_img/1623473867929166.jpg")
	M = cv2.getPerspectiveTransform(rect, dst)
	#with open('./writeYamlData.yml', 'w', encoding='utf-8') as f:
		#yaml.dump(M.tolist(), f,allow_unicode=True)
	np.save('big_test', M)
	#a = np.load('test.npy')
	#print(a)
	size = img.shape[:2]
	proj_img = cv2.warpPerspective(img, M, (size[1],size[0]))
	print(proj_img.shape)
	img_wrap=proj_img[0:1400,400:2100]

	cv2.imwrite('./imgcrop.jpg', img_wrap)
	#proj_img=four_point_transform(img,rect,rect)
	cv2.namedWindow('project img', 0)
	cv2.imshow('project img',img_wrap)

	cv2.waitKey(0)
	

