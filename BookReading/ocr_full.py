#run in python 3
# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import numpy as np
import time
from subprocess import call

from colorthief import ColorThief
import webcolors

cam_ip="rtsp://192.168.43.163:8080/h264_pcm.sdp"
ch=int(input(" 1 for cover page\n 2 for text recognition\n"))
print(type(ch))
if(ch==1):
    
    def closest_colour(requested_colour):
        min_colours = {}
        for key, name in webcolors.css3_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]

    def get_colour_name(requested_colour):
        try:
            closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
            print(closest_name)
        except ValueError:
            closest_name = closest_colour(requested_colour)
            actual_name = None

        return actual_name, closest_name


    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 600,600)
    record_flag = False
    cap = cv2.VideoCapture()
    #cap.open("rtsp://192.168.43.163:8080/h264_pcm.sdp")
    print(cam_ip)
    cap.open(cam_ip)
    while True:
        ret, frame = cap.read()
        cv2.imshow('image', frame)
        #cv2.imshow('test',img)
        if ord('q')==cv2.waitKey(10):
            img_name=str(time.time()) + '.jpg'
            cv2.imwrite(os.path.join('/home/pi/Desktop/Btech_Project/Book_reading/cover/bookcover', img_name),frame)
            color_thief = ColorThief(r'/home/pi/Desktop/Btech_Project/Book_reading/cover/bookcover/'+img_name)

            # get the dominant color
            dominant_color = color_thief.get_color(quality=1)
            print(dominant_color)



            requested_colour = dominant_color
            actual_name, closest_name = get_colour_name(requested_colour)
            cmd_beg= 'espeak -s130 ' 
            cmd_end= ' 2>/dev/null' # To dump the std errors to /dev/null

        
            
            if actual_name is None:
                closest_name="The relative dominant colour of the book cover page is "+closest_name
                print(closest_name)
                text = closest_name.replace(' ', '_')
                #Calls the Espeak TTS Engine to read aloud a Text
                call([cmd_beg+text+cmd_end], shell=True)
            else:
                actual_name="The  dominant colour of the book cover page is "+actual_name
                print(actual_name)
                text = actual_name.replace(' ', '_')
                #Calls the Espeak TTS Engine to read aloud a Text
                call([cmd_beg+text+cmd_end], shell=True)
            break
    #cv2.waitKey(0)
    cap.release()
    #print("hai")
    cv2.destroyAllWindows()

    
elif(ch==2):
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 600,600)
    record_flag = False
    cap = cv2.VideoCapture()
    #cap.open("rtsp://192.168.43.163:8080/h264_pcm.sdp")
    print(cam_ip)
    cap.open(cam_ip)
    while True:
        ret, frame = cap.read()
        cv2.imshow('image', frame)
        #cv2.imshow('test',img)
        if ord('q')==cv2.waitKey(10):
            img_name=str(time.time()) + '.jpg'
            cv2.imwrite(os.path.join('/home/pi/Desktop/Btech_Project/Book_reading', img_name),frame)
            # construct the argument parse and parse the arguments
            ap = argparse.ArgumentParser()
            #ap.add_argument("-i", "--image", required=True,
            #    help="path to input image to be OCR'd")
            ap.add_argument("-p", "--preprocess", type=str, default="thresh",
                help="type of preprocessing to be done")
            args = vars(ap.parse_args())

            # load the example image and convert it to grayscale
            #image = cv2.imread(args["image"])
            image = cv2.imread(img_name)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.namedWindow('Image',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Image', 600,600)
            cv2.imshow("Image", gray)

            # check to see if we should apply thresholding to preprocess the
            # image
            if args["preprocess"] == "thresh":
                gray = cv2.threshold(gray, 0, 255,
                    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

            # make a check to see if median blurring should be done to remove
            # noise
            elif args["preprocess"] == "blur":
                gray = cv2.medianBlur(gray, 3)

            # write the grayscale image to disk as a temporary file so we can
            # apply OCR to it
            filename = "{}.png".format(os.getpid())
            cv2.imwrite(filename, gray)

            # load the image as a PIL/Pillow image, apply OCR, and then delete
            # the temporary file
            text = pytesseract.image_to_string(Image.open(filename))
            os.remove(filename)
            text=text.replace('\n',' ')
            ########text=text.replace('"','')
            ######text=text.replace('“','')
            print(text)
            cmd_beg= 'espeak -s130 ' 
            cmd_end= ' 2>/dev/null' # To dump the std errors to /dev/null
            i=0
            text1=""
            while(i<len(text)):
                if(text[i]=='\n'):
                    #text1+='\0'
                    print(text1)
                    text1 = text1.replace(' ', '_')
                    #Calls the Espeak TTS Engine to read aloud a Text
                    call([cmd_beg+text1+cmd_end], shell=True)
                    text1=""
                    i+=1
                elif(i==len(text)-1):
                    text1+=text[i]
                    print("end"+text1)
                    text1 = text1.replace(' ', '_')
                    #Calls the Espeak TTS Engine to read aloud a Text
                    call([cmd_beg+text1+cmd_end], shell=True)
                    i+=1
                else:
                    text1+=text[i]
                    i+=1          
            #Calls the Espeak TTS Engine to read aloud a Text
            #call([cmd_beg+text1+cmd_end], shell=True)
            #espeak "Text you wish to hear back" 2>/dev/null
            # show the output images
            # cv2.imshow("Image", image)
            cv2.namedWindow('Output',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Output', 600,600)
            cv2.imshow("Output", gray)
            cv2.waitKey(0)

