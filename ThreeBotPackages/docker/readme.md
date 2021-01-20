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

## helm charts

The helm charts are located in the `helm` folder.

## Packaging the charts

Create a "packagedcharts" folder here. It is already in the .gitignore.

Empty the folder if it already existed and in this folder, package the charts you modified:

```sh
helm package ./../tftservices
helm package ./../tftstatistics
```

## Update the index

```sh
curl -O https://raw.githubusercontent.com/threefoldfoundation/helmcharts/main/index.yaml
helm repo index . --merge index.yaml
```

Modify the generated `index.yaml` to point to the right url and upload the helm package and the created `index.yaml.`
