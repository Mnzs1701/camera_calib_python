# camera_calib_python
Documentation for camera calibration using a video

## Install

Install the requirements using:
```
pip3 install -r requirements.txt
```

## Setup

1. Download the following [camera matrix](https://www.mrpt.org/downloads/camera-calibration-checker-board_9x7.pdf)
2. Print the checker board on an A4 sheet
3. Place the checker board on a solid board
4. Record a video while moving the checker board around the visualized frame
5. Save the video into the current directory with the name **calib.mp4** 

## Calibration
Run the calibration script using 

```
python3 cameracalib.py 
```

## Verification
Run verification using 
```
python3 cameraverify.py 
```

The result of the verification should have lesser distortion compared to the raw video