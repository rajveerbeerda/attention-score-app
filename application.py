from flask import Flask, request, Response, jsonify, render_template, make_response, redirect, url_for, flash, sessions, session, get_flashed_messages
import operator
from werkzeug import secure_filename

from threading import Thread

import shutil
import os
import time



from python_files.main import *

import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
app.secret_key = "abcdefgh"


@app.route('/', methods=["GET", "POST"])
def index():
    if os.path.exists(os.path.join('python_files', 'instance')):
        shutil.rmtree(os.path.join('python_files', 'instance'))

    uploads_dir = os.path.join('python_files', 'instance', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)

    audio_dir = os.path.join('python_files', 'instance', 'audios')
    os.makedirs(audio_dir, exist_ok=True)

    frame_dir = os.path.join('python_files', 'instance', 'frames')
    os.makedirs(frame_dir, exist_ok=True)

    video_dir = os.path.join('python_files', 'instance', 'videos')
    os.makedirs(video_dir, exist_ok=True)

    if not os.path.exists(os.path.join('python_files', 'instance', 'time-for-videos.txt')):
        f = open(os.path.join('python_files', 'instance', 'time-for-videos.txt'), "w")
        f.write('0,5')
        f.close()

    if request.method=="POST":
        profile = request.files['myfile']
        profile.save(os.path.join(uploads_dir, secure_filename(profile.filename)))
        return redirect(url_for('leaderboard'))
    return render_template('index.html')

students_grades = {}


@app.route('/_stuff', methods=["GET"])
def stuff():
    f, flag = main_function()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if flag==1:
        name = f[0][0]
        g = {1: "A", 2: "B", 3: "C"}
        grade = g[f[0][1]]
        students_grades[name] = f[0][1]
        return jsonify(name=name, grade=grade, time=current_time, msg='', head='Live attention scores of students:')
    elif flag==-1:
        return jsonify(name='Loading', grade='Loading', time=current_time, msg='Error: Invalid Video Format', head='Invalid video format')
    else:
        s = 0
        for i in students_grades.keys():
            s = s + int(students_grades[i])

        s = s//len(students_grades.keys())
        g = {1: "A", 2: "B", 3: "C"}

        return jsonify(name=list(students_grades.keys())[0], grade=g[s], time=current_time, msg='Grading Done', head='Average attention score of students:')

@app.route('/leaderboard')
def leaderboard():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return render_template('leaderboard.html', no=1, time=current_time)

# @app.route('/leaderboard')
# def leaderboard():
#     text = request.args.get('jsdata')
#     grades, flag = main_function()
#     if flag==1:
#         for std_name in dict(grades).keys():
#             lst = students_grades.grades.get(std_name, [])
#             lst.append(dict(grades)[std_name])
#             students_grades.grades[std_name] = lst
#         g = {1:"A", 2:"B", 3:"C"}
#     else:
#         return redirect(url_for('feedback'))
#     # grades = [('Rajveer_Beerda', 2), ('Kabir_Kohli', 1)]
#
#     return render_template('leaderboard.html', grades=grades, no=len(grades), g=g)

@app.route('/feedback')
def feedback():
    std_grades = students_grades.grades
    print(std_grades)
    # std_grades = {'Manmeet_Sethi': [1, 3, 2, 2, 1, 3]}
    avg_grades = {}
    g = {1: "A", 2: "B", 3: "C"}
    for i in std_grades.keys():
        avg_grades[i] = int(sum(std_grades[i])/len(std_grades[i]))

    sorted_grades = sorted(avg_grades.items(), key=operator.itemgetter(1), reverse=True)
    return render_template('feedback.html', sorted_grades=sorted_grades, n=len(sorted_grades), g=g)

if __name__ == '__main__':
    app.run(debug=False, threaded=False)
    # app.run(debug=True)