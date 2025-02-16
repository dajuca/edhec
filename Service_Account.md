## Google Cloud Platform
### Service Accounts

 ```bash
SERVICE_ACCOUNT=app-sa
DISPLAY_NAME="My App SA"
PROJECT=project-id
 ```

 ```bash
SA=$SERVICE_ACCOUNT@$PROJECT.iam.gserviceaccount.com
 ```

 ```bash
# create a service account
gcloud iam service-accounts create $SERVICE_ACCOUNT --display-name $DISPLAY_NAME

# create and download new service account key
gcloud iam service-accounts keys create ~/key.json --iam-account $SA

gcloud iam service-accounts list                  # list accounts

gcloud iam service-accounts describe $SA          # describe account

gcloud iam service-accounts delete $SA            # delete account

# test code auth
python -c "from google.cloud import storage; \
    buckets = storage.Client().list_buckets(); \
    [print(b.name) for b in buckets]"
 ```

## Service account roles

 ```bash
SERVICE_ACCOUNT=app-sa
PROJECT=project-id
ROLE_OWNER=roles/owner
 ```



 ```bash
SA=$SERVICE_ACCOUNT@$PROJECT.iam.gserviceaccount.com
 ```


 ```bash
# list service account roles for project
gcloud projects get-iam-policy $PROJECT \
    --flatten="bindings[].members" \
    --format="table(bindings.role)" \
    --filter="bindings.members:$SA"

# search users and service accounts with specific role for project
gcloud projects get-iam-policy $PROJECT \
    --flatten="bindings[].members" \
    --format="table(bindings.members)" \
    --filter="bindings.role:$ROLE_OWNER"

# add role to service account for project
gcloud projects add-iam-policy-binding $PROJECT \
    --member="serviceAccount:$SA" \
    --role=$ROLE_OWNER

# remove role from service account for project
gcloud projects remove-iam-policy-binding $PROJECT \
    --member="serviceAccount:$SA" \
    --role=$ROLE_OWNER
 ```


## Service account credentials

 ```bash
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service_account_key.json
 ```
 ```bash
# use service account for code auth on current shell
export GOOGLE_APPLICATION_CREDENTIALS=~/key.json

# display key to verify environment variable content
cat $GOOGLE_APPLICATION_CREDENTIALS

# use service account for code auth on all new shells on a machine zunning `zsh`
echo "export GOOGLE_APPLICATION_CREDENTIALS = ~/key.json" >> ~/.zshrc
 ```

