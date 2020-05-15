## Section 1 Setup Jetson TX2 and Webcamera
## Section 1.1 Ubuntu Containner and Code

## Section 1.2 MQTT mosquitto broker and mosquitto forwarder
Create a bridge:
>  docker network create --driver bridge hw03
Create an alpine linux - based mosquitto container:
>  docker run --name mosquitto --network hw03 -p 1883:1883 -ti alpine sh
>  # we are inside the container now
>  # install mosquitto
>  apk update && apk add mosquitto
>  # run mosquitto
>  /usr/sbin/mosquitto
>  # Press Control-P Control-Q to disconnect from the container

>  # Create an alpine linux - based message forwarder container:
>  docker run --name forwarder --network hw03 -ti alpine sh
>  # we are inside the container now
>  # install mosquitto-clients
>  apk update && apk add mosquitto-clients
>  ping mosquitto
>  # this should work - note that we are referring to the mosquitto container by name
>  mosquitto_sub -h mosquitto -t <some topic>
>  # the above should block until some messages arrive
>  # Press Control-P Control-Q to disconnect from the container
## Section 2 Setup IBM Cloud containers 
