## Section 1 Setup Jetson TX2 and Webcamera
### Section 1.1 Setup Network Bridge
Create bridge hw03
```
docker network create --driver bridge hw03
```
### Section 1.2 Ubuntu Containner and Code
The Dockerfile is called Dockerfile.ubuntu_jtx2. Use Dockerfile to create an image and run the image to create docker with privilege to use the webcamera, on the network of hw03.
```
docker build -t ubuntu_jtx2 -f Dockerfile.ubuntu_jtx2 .
xhost +
docker run -e DISPLAY=$DISPLAY --privileged -v /tmp:/tmp --name ubuntu_jtx2 --privileged --network hw03 -ti ubuntu_jtx2 bash
```
### Section 1.3 MQTT mosquitto broker and mosquitto forwarder

Create alpine linux mosquitto container, with port 1883, on the network hw03, install mosquitto package
```
docker run --name mosquitto --network hw03 -p 1883:1883 -ti alpine sh
apk update && apk add mosquitto
/usr/sbin/mosquitto
# Press Control-P Control-Q to disconnect from the container
```
Create alpine linux forwarder container, on the network he03, install mosquitto-clients package
```
docker run --name forwarder --network hw03 -ti alpine sh
apk update && apk add mosquitto-clients
ping mosquitto
mosquitto_sub -h mosquitto -t face_detect/test
# Press Control-P Control-Q to disconnect from the container
```
### Section 1.4 Run face_detector_1.py code
Get inside the Jetson TX2 ubuntu container (contain name: ubuntu_jtx2), then run face_detector_1.py code.
Inside the Jetson TX2 ubunto container, it should have two files (1) face_detector_1.py (2) haarcascade_frontalface_default.xml. Here we used a public port which is from test.mosquitto.org (5.196.95.208) in the jetson TX2 broker side as well as the ibmCloud broker side. This port number is written in the python code. This code uses openCV to capture the face images and turn it into grey scale and crop the face out. 
```
docker attach ubuntu_jtx2
python3 face_detector_1.py
```
## Section 2 Setup IBM Cloud containers 
### Section 2.1 Create VM or use jumpbox
For this homework, we basically used jumpbox (original VM) directly. It is because we don't run any heavy machine learning task on VM. In the Future, especially for final project, it is highly recommended to spin up a separate VM and mount the object storage (bucket) on the separate VM. 
### Section 2.2 Create object storage and mount bucket on Jumpbox (follow Lab2 steps)
Creat a object storage using ibm UI
download s3fs, bulid and install library
```
sudo apt-get update
sudo apt-get install automake autotools-dev g++ git libcurl4-openssl-dev libfuse-dev libssl-dev libxml2-dev make pkg-config
git clone https://github.com/s3fs-fuse/s3fs-fuse.git
cd s3fs-fuse
./autogen.sh
./configure
make
sudo make install
```
In the IBM Cloud Object storage, go to Service Credentials, New Credential (be sure to check the HMAC checkbox), and then click "view credential". You will see a JSON file, look for the cos_hmac_keys section and find "access_key_id" and "secret_access_key" and run the below commands. I will not disclose my access_key_id and secret_access_key here due to security reasons. 
```
#   "cos_hmac_keys": {
#    "access_key_id": "somekey",
#    "secret_access_key": "somesecretkey"
#  },
# Substitue your values for <Access_Key_ID> and <Secret_Access_Key> in the below command.
echo "<Access_Key_ID>:<Secret_Access_Key>" > $HOME/.cos_creds
chmod 600 $HOME/.cos_creds
```
Create a directory to mount your bucket. This is done in the /mnt directory on Linux, notice the bucket is created in the IBM Cloud UI. 
I will not disclose my bucket name here for security reasons. 
```
sudo mkdir -m 777 /mnt/mybucket
sudo s3fs bucketname /mnt/mybucket -o passwd_file=$HOME/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.us-east.objectstorage.softlayer.net
```

### Section 2.3 create bridge for mqtt borker and ubuntu container
```
docker network create --driver bridge hw03
```
### Section 2.4 setup mqtt broker container
Use Dockerfile.cloud_broker to build the alphine linux docker image. Then create docker for alpine broker on network hw03, with port 1883
```
docker build -t cloud_broker -f Dockerfile.cloud_broker .
docker run --name mosquitto_alpine --network hw03 -p 1883:1883 -ti cloud_broker sh 
```
### Section 2.5 setup ubuntu container for image processing
Use Dockerfile.cloud_ubuntu to build the ubuntu docker image. Then create docker on network hw03, put volume /mnt/mybucket to the folder inside the docker /HW03-faces
```
docker build -t cloud_ubuntu -f Dockerfile.cloud_ubuntu .
docker run --name subscriber --network hw03 -v "/mnt/mybucket":/HW03-faces -ti cloud_ubuntu bash
```
 
### Section 2.6 run face_saver_1.py code
Get into the cloud ubuntu container (container name: subscriber), and run the face_saver_1.py. This code will receive the cropped image from the jetson edge devices and save the image in the bucker on the ibmcloud. 
```
docker attach subscriver
python3 face_saver_1.py
```

