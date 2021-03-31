# TFT backup

## Example as a kubernetes cron job

It uses a persistent volume(for the case of the example, hostPath is used) to write the exported data to and scheduled hourly.

volume.yaml :

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: tftbackup-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  volumeMode: Filesystem
  persistentVolumeReclaimPolicy: Retain
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /mnt/backup/tft
    type: DirectoryOrCreate
```

volumeclaim.yaml:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: tftbackup-pv-claim
spec:
  volumeName: tftbackup-volume
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

cronjob.yaml:

```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: tftbackup
spec:
  schedule: "0 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          volumes:
            - name: tftbackup-pv-storage
              persistentVolumeClaim:
                claimName: tftbackup-pv-claim
          containers:
            - name: tftbackup
              image: tftbackup:1.2.1-rc8
              imagePullPolicy: IfNotPresent
              volumeMounts:
                - name: tftbackup-pv-storage
                  mountPath: "/data"
          restartPolicy: OnFailure
```
