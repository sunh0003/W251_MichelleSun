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

## step 3:

## step 4:
