# Dockerfiles  and kubernetes installs

## TFT services

This container image contains a threebot with all the tft services installed

```sh
docker build tftservices -t tftservices:$(git describe --abbrev=0 --tags | sed 's/^v//') --no-cache
```

If you installed tftservices through the helm chart and want to get inside the pod:
`kubectl exec $(kubectl get pods --selector "app.kubernetes.io/name=tftservices" --output=name) -it /bin/bash`

## Statistics

This container image contains a threebot with the tft_statistics pacxkage installed

```sh
docker build tftstatistics -t tftstatistics:$(git describe --abbrev=0 --tags | sed 's/^v//') --no-cache
```
