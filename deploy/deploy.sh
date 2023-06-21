#!/usr/bin/env sh

set -eux

# Create the namespace
kubectl create namespace $NAMESPACE || true

# Delete Kubernetes secret if exists
kubectl delete secret airflow-service-account airflow-ssh-git-secret airflow-postgresql --namespace $NAMESPACE || true

# Create GCP service account file
cat $GOOGLE_APPLICATION_CREDENTIALS >> ./service-account.json

kubectl create secret generic airflow-ssh-git-secret --namespace $NAMESPACE --from-literal=id_rsa="$AIRFLOW_SSH_SECRET"

kubectl create secret generic airflow-postgresql --namespace $NAMESPACE --from-literal=postgresql-password="$POSTGRES_PASSWORD"

# Recreate service account file as Kubernetes secret
kubectl create secret generic airflow-service-account \
    --namespace $NAMESPACE \
    --from-file=key.json=./service-account.json

helm repo add airflow-stable https://airflow-helm.github.io/charts

helm repo update

helm upgrade \
    --install \
    --debug \
    --create-namespace \
    --namespace "${NAMESPACE}" \
    --wait \
    --version "8.7.1" \
    --timeout 900s \
    -f ./charts/airflow/values.yaml \
    $APP_NAME \
    airflow-stable/airflow

# kubectl create secret generic airflow-ssh-git-secret --namespace airflow --from-file=id_rsa=$HOME/.ssh/id_rsa