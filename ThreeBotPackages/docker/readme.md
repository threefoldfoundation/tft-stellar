# Dockerfiles  and kubernetes installs

If executing docker builds on an Apple Silicon chip, add `--platform linux/amd64`.

## jssdk

Base container with js-sdk installed

```sh
docker build js-sdk -t jssdk:development --no-cache
```

## TFT services

This container image contains a threebot with all the tft services installed

Requires the `jssdk:development` image.

```sh
docker build tftservices -t tftservices:$(git describe --abbrev=0 --tags | sed 's/^v//') --no-cache
```

If you installed tftservices through the helm chart and want to get inside the pod:
`kubectl exec $(kubectl get pods --selector "app.kubernetes.io/name=tftservices" --output=name) -it /bin/bash`

## Statistics

Requires the `jssdk:development` image.

This container image contains a threebot with the tft_statistics package installed

```sh
docker build tftstatistics -t tftstatistics:$(git describe --abbrev=0 --tags | sed 's/^v//') --no-cache
```

## tftbackup

Requires the `jssdk:development` image.

```sh
docker build tftbackup -t tftbackup:$(git describe --abbrev=0 --tags | sed 's/^v//') --no-cache
```

There is an example of deploying this image on kubernetes as a cronjob in the [tftbackup readme](./tftbackup/readme.md)

## helm charts

The helm charts are located in the `helm` folder.

## Packaging the charts

Upgrade the version.

Create a "packagedcharts" folder in the `helm` folder. It is already in the .gitignore.

Empty the folder if it already existed and in this folder, package the charts you modified:

```sh
helm package ./../tftservices
helm package ./../tftstatistics
```

## Update the index

```sh
curl -O https://raw.githubusercontent.com/threefoldfoundation/helmcharts/main/index.yaml
helm repo index . --merge index.yaml --url https://github.com/threefoldfoundation/tft-stellar/releases/download/$(git describe --abbrev=0 --tags)
```

Upload the helm package in the release and the replace the `index.yaml` file in github at threefoldfoundation/helmcharts/index.yaml
