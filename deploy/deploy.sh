#!/usr/bin/env sh

set -eux

# Create the namespace
kubectl create namespace $NAMESPACE || true

# Delete Kubernetes secret if exists
kubectl delete secret matrix-service-account --namespace $NAMESPACE || true

# Create GCP service account file
cat $GOOGLE_APPLICATION_CREDENTIALS >> ./service-account.json

# Recreate service account file as Kubernetes secret
kubectl create secret generic matrix-service-account \
    --namespace $NAMESPACE \
    --from-file=key.json=./service-account.json

helm upgrade \
    --install \
    --debug \
    --create-namespace \
    --namespace "${NAMESPACE}" \
    --set externalDatabase.user="${POSTGRES_USER}"\
    --set externalDatabase.password="${POSTGRES_PASSWORD}"\
    --wait \
    --timeout 300s \
    -f ./charts/matrix/values.yaml \
    $APP_NAME \
    ./charts/matrix
