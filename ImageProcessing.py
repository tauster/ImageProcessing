from __future__ import division, print_function, absolute_import

import numpy as np
import glob
import cv2
import matplotlib.pyplot as plt
import sys

"""
Tausif S., 2017
Processing masked trajectory images.
"""

#---------------------------------------------------------------------
# Grabbing list of images and parsing location data.
#---------------------------------------------------------------------
# Creating list of all the jpg files in the current directory.
img_list = glob.glob("*.jpg")

# Creating an array to store all the file name data.
img_data = np.ones((len(img_list), 5))


# Going through list of the images and parsing data as needed.
for i in range(0, len(img_list)):
	current_img = img_list[i]

	# Splitting the file name to 5 elements separated by "_".
	img_info = current_img.split("_")

	# Removing all other relevant characters not required.
	img_info[1] = img_info[1].replace("t", "")
	img_info[2] = img_info[2].replace("X", "")
	img_info[3] = img_info[3].replace("Y", "")
	img_info[4] = img_info[4].replace("Z", "")
	img_info[4] = img_info[4].replace(".jpg", "")

	# Storing this image's info into the data array as floats.
	img_data[i,:] = [float(k) for k in img_info]


#---------------------------------------------------------------------
# Finding points.
#---------------------------------------------------------------------
# Analyze all images. len(img_list)
for i in range(0, len(img_list)):
	try:
		# Reading and converting to bitwise black/white image.
		img_pre = cv2.imread(img_list[i])
		gray = cv2.cvtColor(img_pre, cv2.COLOR_BGR2GRAY)
		(thresh, mask) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

		# Displays masked image and waits for a key to be pressed.
		cv2.imshow("mask", mask)
		#cv2.imshow("img", img)
		#cv2.imshow("res", res)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

		# Find the contours and hierarchy of the masked image.
		contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		# In the event there's more than 1 ball in an image.
		num_balls = len(contours)

		# Initial centroid holder.
		centroids = np.ones((num_balls, 2))
		
		# Evaluate centroid using the moments output with the ball contours.
		
		for j in range(0, num_balls):
			cont_now = contours[j]
			M = cv2.moments(cont_now)
			# Calculating centroid coordinates using the moments found.
			cx_now = int(M['m10']/M['m00'])
			cy_now = int(M['m01']/M['m00'])

			# Storing the centroid for later use.
			centroids[j, :] = [cx_now, cy_now]
		

		# Retrieving relevant info parsed earlier for current image.
		current_x = img_data[i, 2]
		current_y = img_data[i, 3]
		altitude = img_data[i, 4]
		
		# Calculating the field diadonal with respect to the camera's fiagonal FOV.
		field_diag = 2*((altitude*np.sin(32*(np.pi/180)))/np.sin(58*(np.pi/180)))

		# Calculating x & y lengths in meters using pixel conversion.
		field_x = field_diag*(360/800)
		field_y = field_diag*(640/800)

		# Calculate the overall axes with respect to the current image's location.
		field_x_axis = np.array([current_x - (field_x/2), current_x + (field_x/2)])
		field_y_axis = np.array([current_y - (field_y/2), current_y + (field_y/2)])

		# Converting the pixel centroids into meters centroids and shifting with respect to the UAV's position.
		meters_cent = np.ones((num_balls, 3))
		meters_cent[:, 0] = img_data[i, 0]
		
		meters_cent[:, 1] = centroids[:, 0]*(field_x/360) + field_x_axis[0]
		meters_cent[:, 2] = centroids[:, 1]*(field_y/640) + field_y_axis[0]

		# Saving relevant centroid data to a csv file for reference.
		
		ball_pos_log = np.genfromtxt('traj_points.csv', delimiter = ",")
		N, M = ball_pos_log.shape
		new_log = np.append(ball_pos_log, meters_cent, axis = 0)
		np.savetxt('traj_points.csv', new_log, delimiter = ",")
		

		print(centroids)
		print(meters_cent)
		
		
		plt.imshow(mask)
		plt.plot(centroids[:, 0], centroids[:, 1], 'ro')
		plt.show()
		


	except Exception, e:
		print(str(e))

