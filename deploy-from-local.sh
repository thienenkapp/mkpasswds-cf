#!/bin/bash

#
# Deployment options
#   https://cloud.google.com/sdk/gcloud/reference/functions/deploy#--run-service-account
#

gcloud functions deploy countries \
  --region=europe-west1 \
  --runtime=python310 \
  --source=./src/countries \
  --entry-point=main \
  --trigger-http \
  --allow-unauthenticated \
  --service-account=mkpasswd-firestore@thienenkapp-mkpasswd-001.iam.gserviceaccount.com \
  --update-labels deploy=local \
  --min-instances=0 \
  --max-instances=100 \
  --impersonate-service-account=terraform-iac-pipeline@thienenkapp-mkpasswd-001.iam.gserviceaccount.com \
  --verbosity error

gcloud functions deploy categories \
  --region=europe-west1 \
  --runtime=python310 \
  --source=./src/categories \
  --entry-point=main \
  --trigger-http \
  --allow-unauthenticated \
  --service-account=mkpasswd-firestore@thienenkapp-mkpasswd-001.iam.gserviceaccount.com \
  --update-labels deploy=local \
  --min-instances=0 \
  --max-instances=100 \
  --impersonate-service-account=terraform-iac-pipeline@thienenkapp-mkpasswd-001.iam.gserviceaccount.com \
  --verbosity error

gcloud functions deploy passwords \
  --region=europe-west1 \
  --runtime=python310 \
  --source=./src/passwords \
  --entry-point=main \
  --trigger-http \
  --allow-unauthenticated \
  --service-account=mkpasswd-firestore@thienenkapp-mkpasswd-001.iam.gserviceaccount.com \
  --update-labels deploy=local \
  --min-instances=0 \
  --max-instances=100 \
  --impersonate-service-account=terraform-iac-pipeline@thienenkapp-mkpasswd-001.iam.gserviceaccount.com \
  --verbosity error
