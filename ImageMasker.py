from __future__ import division, print_function, absolute_import

import numpy as np
import glob
import cv2
import matplotlib.pyplot as plt
import sys

"""
Tausif S., 2017
Creating masked images.
"""

#---------------------------------------------------------------------
# Grabbing list of images and parsing location data.
#---------------------------------------------------------------------
# Creating list of all the jpg files in the current directory.
img_list = glob.glob("*.jpg")

#---------------------------------------------------------------------
# Image masker.
#---------------------------------------------------------------------
# Upper and lower HSV colour bounds to isolate the ball colours.
lower_orange = np.array([125, 0, 0])
upper_orange = np.array([200, 255, 150])

# A simple kernel used for the morph and dilate functions.
kernel = np.ones((5,5),np.uint8)

# Analyze all images. len(img_list)
for i in range(0, len(img_list)):
	try:
		# Reading/flipping and converting to HSV image. Flipping to get proper y-coordinates. HSV for better color isolation.
		img = cv2.imread(img_list[i])
		print(img_list[i])
		img = cv2.flip(img, 0)
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		# Creating the masked black and white image with only isolated targets.
		mask = cv2.inRange(hsv, lower_orange, upper_orange)

		# Applying image noise removal and smoothing with the morph and dilate functions.
		# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
		# mask = cv2.dilate(mask, kernel, iterations = 1)

		# Isolated image on top of mask.
		res = cv2.bitwise_and(img, img, mask = mask)

		# Displays masked image and waits for a key to be pressed.
		# cv2.imshow("mask", mask)
		# cv2.imshow("img", img)
		cv2.imshow("res", res)

		file_dir = "/home/tausif/Desktop/Project_test/Masked/" + img_list[i]
		cv2.imwrite(file_dir, res)

		cv2.waitKey(0)
		cv2.destroyAllWindows()


	except Exception, e:
		print(str(e))

