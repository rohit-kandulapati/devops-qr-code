## Running the Dockering Images
```Bash
## creating the docker network
docker network create qrcode

## running frontend image
docker run -d -t -p 3000:3000 --network qrcode --name fe 899f9d3181d0

## running api image
docker run -d -it -p 8000:8000 --network qrcode --name api f5ac8faae619
```
