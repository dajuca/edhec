## Google Cloud Platform
### Cli help

 ```bash
gcloud                                  # command group categories
gcloud --help                           # command flags and groups

gcloud cheat-sheet                      # cheat sheet
 ```


## Code authentication

 ```bash
# authenticate code through user credentials
# generates `~/.config/gcloud/application_default_credentials.json`
gcloud auth application-default login

# prevent environment variable from taking precedence over your credentials in the current shell
unset GOOGLE_APPLICATION_CREDENTIALS
 ```

## Cli setup

 ```bash
# create configuration, run auth login and set default account, project, and compute region and zone
gcloud init
 ```


## Configurations

```bash
CONF=perso
 ```

```bash
gcloud config configurations list                 # list confs
gcloud config configurations create $CONF         # create conf
gcloud config configurations activate default     # activate conf

gcloud config configurations delete $CONF         # delete conf
 ```

## Cli authentication

```bash
gcloud auth list                        # list credentialed accounts
gcloud auth login                       # add credentialed account

gcloud auth revoke --all                # revoke credentialed accounts
 ```


## Active configuration


```bash
EMAIL=you@example.com
PROJECT=project-id
REGION=europe-west1
ZONE=europe-west1-b
 ```
```bash
gcloud config list                      # list active conf parameters

gcloud config set account $EMAIL        # set active conf email
gcloud config set project $PROJECT
gcloud config set compute/region $REGION
gcloud config set compute/zone $ZONE
 ```

## Active configuration parameters


```bash
gcloud projects list                    # list projects

gcloud compute regions list             # list compute regions
gcloud compute zones list               # list compute zones
 ```

## Services


```bash
SERVICE=compute.googleapis.com
 ```
```bash
gcloud services enable $SERVICE         # enable service API

gcloud services list --enabled          # list enabled services
gcloud services list --available        # list available services

gcloud services list --filter=$SERVICE  # verify service status
 ```
