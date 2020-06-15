# Packages import
import sys
import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as paho
from PIL import Image
import sys
import os
import urllib
import tensorflow.contrib.tensorrt as trt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow as tf
import numpy as np
import time
from tf_trt_models.detection import download_detection_model, build_detection_graph

#%matplotlib inline


port_num=1883
broker_addr='5.196.95.208'


# block2 from hint file.  https://github.com/yeephycho/tensorflow-face-detection
url_graph='https://github.com/yeephycho/tensorflow-face-detection/blob/master/model/frozen_inference_graph_face.pb?raw=true'
FROZEN_GRAPH_NAME=wget.download(url_graph)

#block4 load the frozen graph
output_dir=''
frozen_graph = tf.GraphDef()
with open(os.path.join(output_dir, FROZEN_GRAPH_NAME), 'rb') as f:
  frozen_graph.ParseFromString(f.read())

#block5
# https://github.com/NVIDIA-AI-IOT/tf_trt_models/blob/master/tf_trt_models/detection.py
INPUT_NAME='image_tensor'
BOXES_NAME='detection_boxes'
CLASSES_NAME='detection_classes'
SCORES_NAME='detection_scores'
MASKS_NAME='detection_masks'
NUM_DETECTIONS_NAME='num_detections'

input_names = [INPUT_NAME]
output_names = [BOXES_NAME, CLASSES_NAME, SCORES_NAME, NUM_DETECTIONS_NAME]

#block6
trt_graph = trt.create_inference_graph(
    input_graph_def=frozen_graph,
    outputs=output_names,
    max_batch_size=1,
    max_workspace_size_bytes=1 << 25,
    precision_mode='FP16',
    minimum_segment_size=50
)

#block7
tf_config = tf.ConfigProto()
tf_config.gpu_options.allow_growth = True
tf_sess = tf.Session(config=tf_config)

# use this if you want to try on the optimized TensorRT graph
# Note that this will take a while
# tf.import_graph_def(trt_graph, name='')

# use this if you want to try directly on the frozen TF graph
# this is much faster
tf.import_graph_def(frozen_graph, name='')

tf_input = tf_sess.graph.get_tensor_by_name(input_names[0] + ':0')
tf_scores = tf_sess.graph.get_tensor_by_name('detection_scores:0')
tf_boxes = tf_sess.graph.get_tensor_by_name('detection_boxes:0')
tf_classes = tf_sess.graph.get_tensor_by_name('detection_classes:0')
tf_num_detections = tf_sess.graph.get_tensor_by_name('num_detections:0')



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

client.loop_start()

imgid=1
while(True):
    # Capture frame-by-frame from feed
    ret, frame = cap.read()
    image_resized=cv.resize(frame,(300,300))
    image=np.array(frame)

    scores, boxes, classes, num_detections = tf_sess.run([tf_scores, tf_boxes, tf_classes, tf_num_detections], feed_dict={tf_input: image_resized[None, ...]})

    boxes = boxes[0] # index by 0 to remove batch dimension
    scores = scores[0]
    classes = classes[0]
    num_detections = num_detections[0]

    
    # suppress boxes that are below the threshold.. 
    DETECTION_THRESHOLD = 0.5

    # plot boxes exceeding score threshold
    for i in range(int(num_detections)):
        if scores[i] < DETECTION_THRESHOLD:
            continue
        print('scores:', scores[i])
        print('classes:', classes[i])

        # scale box to image coordinates
        box = boxes[i] * np.array([image.shape[0], image.shape[1], image.shape[0], image.shape[1]])
        box = box.astype(int)
        print('Box: ',box)

        cv.rectangle(image,(box[1].box[0]),(box[3],box[2]),(0,255,0),2)
        crop_faces=image_resized[box[0]:box[2],box[1]:box[3]]

        name = 'hw7_faces_'+str(imgid)+'.png'

        cv.imwrite(name, image)
        img_saved=cv.imread('hw7_faces_'+str(imgid)+'.png')
        cv.imshow('object detection', img_saved)

        #publish to MQTT
        pub_resp=client.publish("face_detect/test", bytearray(cv.imencode('.png', image)[1]), qos=1)
    imgid+=1
    plt.show()

    # Close the connection
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Here add Time to wait next command
time.sleep(1) 
tf_sess.close()        
#Here end the loop and disconnect from client
client.loop_stop()
client.disconnect()
cap.release()
cv.destroyAllWindows()







