# FastaAPI demo #

Simple fastapi implementation with docker and sqlite:
- Application does not have any authentication or authorization
- No volume data for database retention

#### Not production ready ####

## Usage ##

build docker image
```
docker build -t fastapi_demo .
```
run docker image
```
docker run -d --name fastapi_demo -p 80:80 fastapi_demo
```



