import cv2
from python_files.gaze_tracking import GazeTracking

def eye_tracking(image_path):
    gaze = GazeTracking()
    frame = cv2.imread(image_path)
    gaze.refresh(frame)

    frame = gaze.annotated_frame()

    if gaze.is_right():
        value = 0.5
    elif gaze.is_left():
        value = 0.5
    elif gaze.is_center():
        value = 1
    else:
        value = 0
    return value

