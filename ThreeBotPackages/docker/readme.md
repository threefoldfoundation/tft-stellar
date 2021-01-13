# Dockerfiles for the ThreefoldFoundation services

This container image contains a threebot with all the tft services installed

```sh
docker build . -t tftservices:$(git describe --abbrev=0 --tags | sed 's/^v//') --no-cache
```

If you installed tftservices through the helm chart and want to get inside the pod:
`kubectl exec $(kubectl get pods --selector "app.kubernetes.io/name=tftservices" --output=name) -it /bin/bash`
