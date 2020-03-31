from pathlib import Path
import os
import operator
from datetime import datetime

from python_files.video_edits import *
from python_files.eye_tracking import *
from python_files.facial_expressions_recognizer import *
from python_files.detect_voice import *

import time

import warnings
warnings.filterwarnings("ignore")

uploads_dir = os.path.join('python_files', 'instance', 'uploads')
audio_dir = os.path.join('python_files', 'instance', 'audios')
frame_dir = os.path.join('python_files', 'instance', 'frames')
video_dir = os.path.join('python_files', 'instance', 'videos')

def main_function():
    ########################################################################################################

    student_names = []
    video_durations = []
    for item in Path(uploads_dir).iterdir():
        if item.is_file():
            s = str(item.name)[-3:]
            if s=="mov" or s=='mp4' or s=='wmv' or s=='avi' or s=='mpg' or s=='flv':
                student_names.append(str(item.name).split('.')[0])
                # video_durations.append(video_duration(os.path.join(uploads_dir, item.name)))
                min_video_duration = video_duration(os.path.join(uploads_dir, item.name))
            else:
                return {}, -1

    # min_video_duration = min(video_durations)

    ########################################################################################################

    f = open("python_files/instance/time-for-videos.txt", "r")
    s = str(f.read()).split(",")
    f.close()

    start_time = int(s[0])
    end_time = int(s[1])

    f = open("python_files/instance/time-for-videos.txt", "w")
    if end_time>min_video_duration:
        f.write(str(start_time) + "," + str(end_time))
        f.close()
        return {}, 0
    else:
        f.write(str(end_time + 1) + "," + str(end_time + 5))
    f.close()

    ########################################################################################################

    for student_name in student_names:
        frame_path = os.path.join(frame_dir, student_name)
        if not os.path.isdir(frame_path):
            os.mkdir(frame_path)
        path = os.path.join(uploads_dir, student_name + ".mov")
        trim_video(path, start_time, end_time)
        video_to_audio(os.path.join(video_dir, student_name + ".mov"))
        video_to_frames(os.path.join(video_dir, student_name + ".mov"))

    ########################################################################################################


    eye_values = {}
    face_values = {}
    audio_values = {}

    for student_name in student_names:
        frame_path = os.path.join(frame_dir, student_name)
        for item in Path(frame_path).iterdir():
            if item.is_file():
                s = str(item.name)[-3:]
                if s == "jpg":
                    image_path = os.path.join(frame_path, str(item.name))
                    lst = eye_values.get(student_name, [])
                    lst.append(eye_tracking(image_path))
                    eye_values[student_name] = lst
                    lst = face_values.get(student_name, [])
                    lst.append(facial_expressions_recognizer(image_path))
                    face_values[student_name] = lst

        audio_path = os.path.join(audio_dir, student_name + ".wav")
        # audio_values[student_name] = detect_voice(audio_path)

    grade_values = grading(eye_values, face_values)
    sorted_grades = sorted(grade_values.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_grades, 1

def grading(eye_values, face_values):
    # names = audio_values.keys()
    names = eye_values.keys()
    grades = {}
    # for i in names:
    #     if audio_values[i]==1:
    #         grades[i] = 1
    #     else:
    #         if face_values[i][0]!=face_values[i][1]:
    #             grades[i] = 2
    #         else:
    #             if eye_values[i][0]==1 and eye_values[i][1]==1:
    #                 grades[i] = 2
    #             else:
    #                 grades[i] = 3

    for i in names:
        if face_values[i][0]!=face_values[i][1]:
            grades[i] = 1
        else:
            if eye_values[i][0]==1 and eye_values[i][1]==1:
                grades[i] = 2
            else:
                grades[i] = 3
    return grades

# print(main_function())