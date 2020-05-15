## Section 1 Setup Jetson TX2 and Webcamera
## Section 1.1 Ubuntu Containner and Code

## Section 1.2 MQTT mosquitto broker and mosquitto forwarder
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
## Section 2 Setup IBM Cloud containers 
