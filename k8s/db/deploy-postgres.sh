#!/bin/bash

NAMESPACE="sensor-app"

echo "Deleting existing resources..."
kubectl delete deployment postgres -n $NAMESPACE --ignore-not-found
kubectl delete pvc postgres-pvc -n $NAMESPACE --ignore-not-found
kubectl delete configmap postgres-init-sql -n $NAMESPACE --ignore-not-found

echo "Creating PersistentVolumeClaim..."
kubectl apply -f postgres-pvc.yaml

echo "Waiting for PVC to be bound..."
while [[ $(kubectl get pvc postgres-pvc -n $NAMESPACE -o jsonpath='{.status.phase}') != "Bound" ]]; do
  echo -n "."
  sleep 2
done
echo " PVC Bound!"

echo "Creating ConfigMap..."
kubectl apply -f db-init-configmap.yaml

echo "Deploying Postgres..."
kubectl apply -f db-deployment.yaml

echo "Waiting for Postgres pod to be running..."
while [[ $(kubectl get pods -n $NAMESPACE -l app=postgres -o jsonpath='{.items[0].status.phase}') != "Running" ]]; do
  echo -n "."
  sleep 3
done
echo " Postgres pod is Running!"

echo "Done!"

