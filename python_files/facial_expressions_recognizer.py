from keras.models import load_model
import cv2
import numpy as np

import warnings
warnings.filterwarnings("ignore")

MODEL_PATH = 'python_files/models/pretrained.h5'
model = load_model(MODEL_PATH)
model._make_predict_function()

def model_predict(img_path, model):
    cv2.ocl.setUseOpenCL(False)
    emotion_dict = {1: "Angry", 2: "Disgusted", 3: "Fearful", 4: "Happy", 5: "Neutral", 6: "Sad", 7: "Surprised"}
    facecasc = cv2.CascadeClassifier('python_files/haarcascade_frontalface_default.xml')
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    if len(faces)!=0:
        try:
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                prediction = model.predict(cropped_img)
                maxindex = int(np.argmax(prediction))
                cv2.putText(img, emotion_dict[maxindex], (x + 20, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                            cv2.LINE_AA)
            return maxindex
        except Exception as e:
            return 0
    else:
        return 0

def facial_expressions_recognizer(image_path):
    return model_predict(image_path, model)