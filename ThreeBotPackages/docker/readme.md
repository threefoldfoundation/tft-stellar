# Dockerfiles for the ThreefoldFoundation services

This container image contains a threebot with all the tft services installed

```sh
docker build . -t tftservices:$(git describe --abbrev=0 --tags | sed 's/^v//') --no-cache
```
