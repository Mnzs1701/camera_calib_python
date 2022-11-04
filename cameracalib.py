import pickle
import cv2
import numpy as np
import os
import glob
 
 
# Define the dimensions of checkerboard
CHECKERBOARD = (7, 9)
#Download the checkerboard from https://www.mrpt.org/downloads/camera-calibration-checker-board_9x7.pdf
 
 
# stop the iteration when specified
# accuracy, epsilon, is reached or
# specified number of iterations are completed.
criteria = (cv2.TERM_CRITERIA_EPS +
            cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
 
# Vector for 3D points
threedpoints = []
 
# Vector for 2D points
twodpoints = []
 
 
#  3D points real world coordinates
objectp3d = np.zeros((1, CHECKERBOARD[0]
                      * CHECKERBOARD[1],
                      3), np.float32)
objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0],
                               0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None
 
 
# Set the path to the video files 
vidcap = cv2.VideoCapture('calib.mp4')
success,image = vidcap.read()

count = 0
drop_frame = 1 # Look at every n'th frame of the video 
# Higher drop frame=> Faster program but lower quality matrix
# Lower drop frame=> Slower program but better matrix

while success and (count < 1000):
    success,image = vidcap.read()
    # print('Read a new frame: ', success)

    if not success:
        break

    count += 1
    if count%drop_frame == 0:

        grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        # If desired number of corners are found in the image then ret = true
        ret, corners = cv2.findChessboardCorners(
                        grayColor, CHECKERBOARD,
                        cv2.CALIB_CB_ADAPTIVE_THRESH
                        + cv2.CALIB_CB_FAST_CHECK +
                        cv2.CALIB_CB_NORMALIZE_IMAGE)
    
        # If desired number of corners can be detected then,
        # refine the pixel coordinates and display them on the images of checker board
        if ret == True:
            threedpoints.append(objectp3d)
    
            # Refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(
                grayColor, corners, (11, 11), (-1, -1), criteria)
    
            twodpoints.append(corners2)
    
            # Draw and display the corners
            image = cv2.drawChessboardCorners(image,
                                            CHECKERBOARD,
                                            corners2, ret)
    
        cv2.imshow('img', image)
        cv2.waitKey(10)
 
cv2.destroyAllWindows()
 
 
print("Processing the data...This step may take a few minutes...")

# Perform camera calibration by passing the value of above found out 3D points (threedpoints)
# and its corresponding pixel coordinates of the detected corners (twodpoints)
ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
    threedpoints, twodpoints, grayColor.shape[::-1], None, None)
 
 
# Displaying required output
print(" Camera matrix:")
print(matrix)
 
print("\n Distortion coefficient:")
print(distortion)
 
print("\n Rotation Vectors:")
print(r_vecs)
 
print("\n Translation Vectors:")
print(t_vecs)

calib_data = [matrix,distortion,r_vecs,t_vecs]

with open('calibfile.txt', 'wb') as fh:
   pickle.dump(calib_data, fh)