# Camera Undistort
import cv2
import numpy as np
import os
import glob
import pickle

pickle_reader = open ("calibfile.txt", "rb")
calibdata = pickle.load(pickle_reader)

matrix, distortion,r_vecs,t_vecs = calibdata

print(" Camera matrix:")
print(matrix)
 
print("\n Distortion coefficient:")
print(distortion)
 
print("\n Rotation Vectors:")
print(r_vecs)
 
print("\n Translation Vectors:")
print(t_vecs)

vidcap = cv2.VideoCapture('calib.mp4')
success,image = vidcap.read()

count = 0
while success and (count < 1000):
    success,image = vidcap.read()
    # print('Read a new frame: ', success)

    if not success:
        break

    count += 1
    h,  w = image.shape[:2]
    if count == 1:
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(np.float32(matrix), np.float32(distortion), (w,h), 1, (w,h))
    # undistort
    imrec = cv2.undistort(image, np.float32(matrix), np.float32(distortion), None, newcameramtx)
    # crop the image
    x, y, w, h = roi
    numpy_horizontal = np.hstack((image, imrec))
    imS = cv2.resize(numpy_horizontal, (1280, 720))                # Resize image

    cv2.imshow('img', imS)
    cv2.waitKey(10)
 
cv2.destroyAllWindows()
 
