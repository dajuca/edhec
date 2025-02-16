## Goal
Save the planet saving electricity consumption (and 💰) by learning how to setup a scheduler to shutdown your virtual machine on Google Compute Engine (GCE) every evening at 7PM.

## Context
You set up a working environment on a Compute Engine instance (==virtual machine) and you are fine with it. You learnt EDHEC's best practices 
so every evening before you finish work, you commit your code and push it on GitHub 💯. Your problem is you often (always) forget to stop your instance, 
causing 2 major issues:

The waste of electricity because your VM runs for nothing
The loss of money because Google Cloud Platform (GCP) invoices you on the running time

## Prerequisites
- A GCP project with [Compute Engine API](https://cloud.google.com/compute) enabled
- A GCE instance up and running
- The `gcloud` CLI installed
- Having `gcloud` authenticated on the GCP project hosting the GCE instance
- A service account linked to GCE 👉 [IAM](https://cloud.google.com/iam)
- 
## Create an instance schedule
Resources: [GCE doc](https://cloud.google.com/compute/docs/instances/schedule-instance-start-stop#operation_schedules)

Open your favorite terminal then define the following environment variables:

```bash
# Set your project id
PROJECT_ID=of-your-projet
# You should have a default service account linked to GCE
# Don't know your service account key? Check it with `gcloud iam service-accounts list --project=${PROJECT_ID}`
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='get(projectNumber)')
SERVICE_ACCOUNT=service-$PROJECT_NUMBER@compute-system.iam.gserviceaccount.com
# Set your VM instance name
VM_NAME=de-bootcamp-vm
# Name your scheduler (you can keep the name)
SCHEDULER_NAME=vm-stopper
# Available regions: gcloud compute regions list
REGION=europe-west1
# Available zones within a region: gcloud compute zones list --filter='(region:'$REGION')'
ZONE=europe-west1-b
# Available timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIMEZONE='Europe/Paris'
```

1. Create the `vm-stopper` scheduler:
❗ Make sure your config is set to the right project ID. You can check that by running gcloud config in the terminal.

If a different project ID is currently set, you can change that with: `gcloud config set project $PROJECT_ID`

```bash
gcloud compute resource-policies create instance-schedule $SCHEDULER_NAME \
    --description='Stop the VM every day at 7PM in case of oversight' \
    --region=$REGION \
    --vm-stop-schedule='0 19 * * *' \
    --timezone=$TIMEZONE
```

2. Check that the scheduler has been created:

```bash
gcloud compute resource-policies describe $SCHEDULER_NAME \
    --region=$REGION
```

3. Add the compute instance admin role to the service account:
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$SERVICE_ACCOUNT --role='roles/compute.instanceAdmin'
```
4. Check that the role `compute.instanceAdmin` has been added to the service account:
```bash
gcloud projects get-iam-policy $PROJECT_ID
```

5. Attach the scheduler to the VM
```bash
gcloud compute instances add-resource-policies $VM_NAME \
    --resource-policies=$SCHEDULER_NAME \
    --zone=$ZONE
```

**Great job! Your are now free to forget to stop your VM manually 👍.**
