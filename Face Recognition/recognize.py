import cv2
import json
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from subprocess import call

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
    # Converting image to gray-scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detecting features in gray-scale image, returns coordinates, width and height of features
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    # drawing rectangle around the feature and labeling it
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        # Predicting the id of the user
        id, _ = clf.predict(gray_img[y:y+h, x:x+w])
        ####

        with open('dict.json') as json_file:
            data = json.load(json_file)
        cv2.putText(img, data[str(id)], (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        print(data[str(id)])
        name_person=data[str(id)]+"is here"
        
        cmd_beg= 'espeak -s130 ' 
        cmd_end= ' 2>/dev/null'
        text = name_person.replace(' ', '_')
        #Calls the Espeak TTS Engine to read aloud a Text
        call([cmd_beg+text+cmd_end], shell=True)
        ####
        # Check for id of user and label the rectangle accordingly
        # if id==1:
        #     cv2.putText(img, "Unknown", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        # elif id==2:
        #     cv2.putText(img, "Gandhi", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        # elif id==3:
        #     cv2.putText(img, "modi", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]

    return coords

# Method to recognize the person
def recognize(img, clf, faceCascade):
    color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0), "white": (255, 255, 255)}
    coords = draw_boundary(img, faceCascade, 1.1, 10, color["white"], "Face", clf)
    return img


# Loading classifier
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Loading custom classifier to recognize
clf = cv2.face.LBPHFaceRecognizer_create()
clf.read("classifier.yml")

# Capturing real time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
#video_capture = cv2.VideoCapture(0)
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(320, 240))
display_window = cv2.namedWindow("face detection")
# allow the camera to warmup
time.sleep(0.1)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    img = frame.array
    img = recognize(img, clf, faceCascade)
    # Writing processed image in a new window
    cv2.imshow("face detection", img)
    key = cv2.waitKey(1)

    rawCapture.truncate(0)

    if key == 27:
        camera.close()
        cv2.destroyAllWindows()
        break
