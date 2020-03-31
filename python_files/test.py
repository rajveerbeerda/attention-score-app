from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *

import cv2
import os


def video_duration(video_path):
    clip = VideoFileClip(video_path)
    return clip.duration

def trim_video(video_path, start_time, end_time):
    file_name = video_path.split('/')[-1]
    ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=os.path.join('instance', 'videos', file_name))

def video_to_audio(video_path):
    file_name = str(video_path.split('/')[-1]).split('.')[0]
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(os.path.join('instance', 'audios', file_name + '.wav'))

def video_to_frames(video_path):
    file_name = str(video_path.split('/')[-1]).split('.')[0]
    cam = cv2.VideoCapture(video_path)
    currentframe = 0
    lst = [10, 150]
    while True:
        ret, frame = cam.read()
        if ret:
            if currentframe in lst:
                name = os.path.join('instance', 'frames', file_name, 'frame' + str(currentframe) + '.jpg')
                cv2.imwrite(name, frame)
            currentframe += 1
        else:
            break
    cam.release()
    cv2.destroyAllWindows()
