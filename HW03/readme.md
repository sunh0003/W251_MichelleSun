## Section 1 Setup Jetson TX2 and Webcamera
### Section 1.1 Ubuntu Containner and Code

### Section 1.2 MQTT mosquitto broker and mosquitto forwarder
Create bridge hw03
```
docker network create --driver bridge hw03
```
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
mosquitto_sub -h mosquitto -t <some topic>
# Press Control-P Control-Q to disconnect from the container
```
### Section 1.3 Run face_detector.py code
## Section 2 Setup IBM Cloud containers 
### Section 2.1 Create VM or use jumpbox

### Section 2.2 Mount

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
 
### Section 2.6 run face_subscriber.py code
