#!/bin/bash

# Build and Push Docker Image for ShodhAI Platform

set -e

# Configuration
APP_ACR_NAME="shodhairegistry"
IMAGE_NAME="shodhai-app"
TAG="${1:-latest}"

echo "Building Docker image for ShodhAI..."
echo "Tag: $TAG"
echo ""

# Login to ACR
echo "Logging in to Azure Container Registry..."
az acr login --name $APP_ACR_NAME

# Build image for linux/amd64 (required for Azure Container Apps)
echo "Building Docker image for linux/amd64..."
docker build --platform linux/amd64 -t ${APP_ACR_NAME}.azurecr.io/${IMAGE_NAME}:${TAG} .

# Push to ACR
echo "Pushing image to ACR..."
docker push ${APP_ACR_NAME}.azurecr.io/${IMAGE_NAME}:${TAG}

echo ""
echo "Build and push complete!"
echo "Image: ${APP_ACR_NAME}.azurecr.io/${IMAGE_NAME}:${TAG}"
echo ""
echo "Now run your Jenkins pipeline to deploy."
