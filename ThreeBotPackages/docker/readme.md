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

## jssdk

Base container with js-sdk installed

```sh
docker build js-sdk -t jssdk:development --no-cache
```

## tftbackup

Requires the `jssdk:development` image.

```sh
docker build tftbackup -t tftbackup:$(git describe --abbrev=0 --tags | sed 's/^v//') --no-cache
```

There is an example of deployinmg this image on kubernetes as a cronjob int the [tftbackup readme](./tftbackup/readme.md)


## helm charts

The helm charts are located in the `helm` folder.

## Packaging the charts

Upgrade the version if working on alpha's,beta's or releasecandidates of the chart you are working on.

Create a "packagedcharts" folder here. It is already in the .gitignore.

Empty the folder if it already existed and in this folder, package the charts you modified:

```sh
helm package ./../tftservices --appversion $(git describe --abbrev=0 --tags | sed 's/^v//')
helm package ./../tftstatistics --appversion $(git describe --abbrev=0 --tags | sed 's/^v//')
```

If packaging a semver version, there is no need to upgrade the helm vhart version manually, execute the required commands, setting the chart version to the semver git tag:

```sh
helm package ./../tftservices --appversion $(git describe --abbrev=0 --tags | sed 's/^v//') --version $(git describe --abbrev=0 --tags | sed 's/^v//') 
helm package ./../tftstatistics --appversion $(git describe --abbrev=0 --tags | sed 's/^v//') --version $(git describe --abbrev=0 --tags | sed 's/^v//') 
```

## Update the index

```sh
curl -O https://raw.githubusercontent.com/threefoldfoundation/helmcharts/main/index.yaml
helm repo index . --merge index.yaml --url https://github.com/threefoldfoundation/tft-stellar/releases/download/$(git describe --abbrev=0 --tags)/
```

Upload the helm package in the release and the replace the `index.yaml` file in github at threefoldfoundation/helmcharts/index.yaml
