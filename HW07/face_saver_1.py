import sys
import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as paho

broker_addr = "5.196.95.208"
output_dir ="/HW03-faces/"
port_num = 1883
                        
# Create methods for connections and subscription of messages
def on_connect(client, userdata, flags, rc):
    print("Connected to broker with result code "+str(rc))
    client.subscribe("face_detect/test")

# Start counter
img_cnt = 0

def on_message(client, userdata, msg):
    # check we got the image
    global img_cnt
    print("The image is captured!")
                    
    # De-encode message
    f = np.frombuffer(msg.payload, dtype='uint8')
    img = cv.imdecode(f, flags=1)
    print(img.shape)
                                        
    # Save messages, print image name
    img_name = output_dir + "/face-" + str(img_cnt) + ".png"
    print(img_name)
    img_cnt += 1
                                                                                                    
    # Write image in Object Storage - bucker
    cv.imwrite(img_name, img)
# Connect to MQTT client
client= paho.Client()
client.connect(broker_addr, port_num , 60)
client.on_connect = on_connect
client.on_message = on_message

# Keep this open until streams ends
client.loop_forever()
