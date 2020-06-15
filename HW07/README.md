## step 1: 

we already created the network for hw3, i will continue to use this network
```
docker network create --driver bridge hw03
```

## step 2:

```
docker build -t tensor_face_hw07 -f Dockerfile_TensorHW07 .
docker run --name tensor_face_hw07 --network hw03 -e DISPLAY=$DISPLAY --privileged -v /tmp:/tmp --rm -ti tensor_face_hw07 bash
```

## step 3: Turn on mosquitto and forward

```
docker run --name mosquitto --network hw03 -p 1883:1883 -ti alpine sh
apk update && apk add mosquitto
/usr/sbin/mosquitto
# Press Control-P Control-Q to disconnect from the container

docker run --name forwarder --network hw03 -ti alpine sh
apk update && apk add mosquitto-clients
ping mosquitto
mosquitto_sub -h mosquitto -t face_detect/test
# Press Control-P Control-Q to disconnect from the container
```

## step 4:
