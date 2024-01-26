#!/bin/bash

if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Running the image using docker run..."

    if command -v docker &> /dev/null; then
        docker run -p 8080:8080 sauravschandra/simple_file_store:latest > /dev/null 2>&1 &
        echo "File store server started using docker run."
    else
        echo "Error: docker is not installed. Please install docker and try again."
        exit 1
    fi
else
    kubectl apply -f deploy-template.yaml

    while [[ $(kubectl get pods -l app=simple-file-store -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do
        echo "Waiting for the pod to be ready..."
        sleep 5
    done

    kubectl port-forward service/simple-file-store-service 8080:8080 > /dev/null 2>&1 &
    echo "File store server started using kubectl port-forward."
fi
