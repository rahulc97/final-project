import cv2
import json
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# Method to generate dataset to recognize a person
img_id=0
def generate_dataset(img, id):
    global img_id
    img_id+=1
    if img_id % 50 == 0:
        print("Collected ", img_id, " images")
    # write image in data dir
    cv2.imwrite("data/user."+str(id)+"."+str(img_id)+".jpg", img)
    #return img_id

# Method to draw boundary around the detected feature
def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    # Converting image to gray-scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detecting features in gray-scale image, returns coordinates, width and height of features
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    # drawing rectangle around the feature and labeling it
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]
    return coords

# Method to detect the features
def detect(img, faceCascade):
    color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
    coords = draw_boundary(img, faceCascade, 1.1, 10, color['blue'], "Face")
    # If feature is detected, the draw_boundary method will return the x,y coordinates and width and height of rectangle else the length of coords will be 0
    if len(coords)==4:
        # Updating region of interest by cropping image
        roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
        # Assign unique id to each user
        #user_id = 2
        # img_id to make the name of each image unique
        generate_dataset(roi_img, user_id)

    return img


# Loading classifiers
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


# Capturing real time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
#video_capture = cv2.VideoCapture(0)

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(320, 240))

display_window = cv2.namedWindow("face detection")


# Initialize img_id with 0
#img_id = 0
f = open("current_user_id.txt", "r")
user_id=int(f.read())+1
f.close()
f=open("current_user_id.txt","w")
f.write(str(user_id))
f.close()

print(user_id)

user_name = input("Enter User name")
with open('dict.json') as json_file:
    data = json.load(json_file)
data[user_id]=user_name
json1 = json.dumps(data)
with open('dict.json','w') as json_file:
    json_file.write(json1)
i=input("pause")

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    img = frame.array
    # Call method we defined above
    img = detect(img, faceCascade)
    # Writing processed image in a new window
    cv2.imshow("face detection", img)
    #img_id += 1
    key = cv2.waitKey(1)

    rawCapture.truncate(0)

    if key == 27:
        camera.close()
        cv2.destroyAllWindows()
        break

    
