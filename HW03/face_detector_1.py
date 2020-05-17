"""""""""""""""""""""""""""""""""
Detect faces from USB video camera input in a constant stream. Will publish faces to broker_addr
"""""""""""""""""""""""""""""""""


# Packages import
import sys
import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as paho

port_num=1883
broker_addr='5.196.95.208'

    
# on_connect function to check if connection wih broker is build
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connect to broker")
    else:
        print("Failt to connect to broker")
        
# Connect to client
client = paho.Client()
client.on_connect = on_connect
client.connect(broker_addr, port_num, 60)

# here add time to wait next command, avoid any connection issue
time.sleep(1) 

# Use webcam to capture video
cap = cv.VideoCapture(0)

# XML classifier for face detection
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# Start stream, using loop
client.loop_start()

while(True):
    # Capture frame-by-frame from feed
    ret, frame = cap.read()

    # convert the video to grey
    grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey, 1.3, 5)
    
    # Display image, faces, and publish message
    img = cv.imshow('frame', grey)
    for (x,y,w,h) in faces:
        crop_faces = grey[y:y+h,x:x+w]
        cv.imshow("crop", crop_faces)
        client.publish("face_detect/test", bytearray(cv.imencode('.png', crop_faces)[1]), qos=1)

    # Close the connection
    if cv.waitKey(1) & 0xFF == ord('q'):

        break

# Here add Time to wait next command
time.sleep(1) 
        
#Here end the loop and disconnect from client
client.loop_stop()
client.disconnect()
cap.release()
cv.destroyAllWindows()
