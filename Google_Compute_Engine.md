## Google Compute Engine
### Service
 ```bash
SERVICE=compute.googleapis.com
 ```
 ```bash

gcloud services enable $SERVICE         # enable compute service
 ```

## Location

 ```bash
gcloud compute regions list             # list compute regions
gcloud compute zones list               # list compute zones
 ```

## Hardware

 ```bash
ZONE=europe-west1-b
 ```

 ```bash
# list machine types
gcloud compute machine-types list --filter "zone:($ZONE)"

# list accelerator types
gcloud compute accelerator-types list --filter "zone:($ZONE)"
 ```

## Virtual machines

```bash
INSTANCE=vm-instance
PROJECT=project-id
ZONE=europe-west1-b
IMAGE_PROJECT=ubuntu-os-cloud
IMAGE_FAMILY=ubuntu-2204-lts

 ```

```bash
# list ubuntu available images
gcloud compute images list \
    --project $IMAGE_PROJECT \
    --no-standard-images

# create instance
gcloud compute instances create \
    $INSTANCE \
    --project $PROJECT \
    --zone $ZONE \
    --image-project=$IMAGE_PROJECT \
    --image-family=$IMAGE_FAMILY

# delete instance
gcloud compute instances delete $INSTANCE
 ```

## Status

```bash
INSTANCE=vm-instance
 ```

```bash
gcloud compute instances list                     # list vm status

gcloud compute instances start $INSTANCE          # start instance
gcloud compute instances stop $INSTANCE           # stop instance
 ```

## Remote connection


```bash
INSTANCE=vm-instance
 ```
```bash
# interactive ssh to remote instance
gcloud compute ssh $INSTANCE

# run remote command on remote instance
gcloud compute ssh $INSTANCE --command "ls -la"
 ```

## Remote copy


```bash
INSTANCE=vm-instance
 ```
```bash
# copy recursively home directory on instance to local directory
gcloud compute scp --recurse $INSTANCE:~/ .
 ```

## RIP adress


```bash
INSTANCE=vm-instance
 ```
```bash
# retrieve instance public IP address
gcloud compute instances describe $INSTANCE \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
 ```
