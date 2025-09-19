#!/bin/bash

# Cross-platform Docker runner for AWS Log Checker Helper
# No X11/XQuartz required - runs as web application

echo "Starting AWS Log Checker Helper as web application..."
echo "This will be accessible at http://localhost:8080"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build and run the container
echo "Building Docker container..."
docker build -t helperapp-aws-log-helper .

echo "Starting web server..."
docker run --rm -it -p 8080:8080 helperapp-aws-log-helper

echo "Application has stopped."