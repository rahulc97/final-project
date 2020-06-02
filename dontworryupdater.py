import threading

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# Python program to translate
# speech to text and text to speech

import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

print("Starting")
# Function to convert text to
# speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


# Create an Event for notifying main thread.
callback_done = threading.Event()

cred = credentials.Certificate('custom-location-fe592-5da198800f20.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'messages').document(u'rpi')
doc_ref1 = db.collection(u'messages').document(u'android')

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        # print(u'Received document snapshot: {}'.format(doc.id))
        doc=doc_ref1.get()
        message=doc.to_dict()['message']
        print('\nMessage: {}'.format(message))
        SpeakText(message)
    callback_done.set()


def send_message():
    # Loop infinitely for user to
    # speak

    while (1):

        # Exception handling to handle
        # exceptions at the runtime
        try:

            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("listening...")
                # listens for the user's input
                audio2 = r.listen(source2)
                print("over...")
                # Using ggogle to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()


                now = datetime.now()
                timestamp = now.strftime("%I:%M %p")
                time24=now.strftime("%H:%M:%S")
                print("timestamp =", timestamp)
                doc_ref.set({
                    u'message': MyText,
                    u'time': timestamp,
                    u'time24':time24

                })
                print("Successfully updated")

                print("Did you say " + MyText)
                SpeakText("You said "+MyText)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occured")


# Watch the document
doc_watch = doc_ref1.on_snapshot(on_snapshot)

t1 = threading.Thread(target=send_message())
t1.start()



