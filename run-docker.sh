#!/bin/bash

# Cross-platform Docker runner for AWS Log Checker Helper
# No X11/XQuartz required - runs as web application
# Now with persistent data storage and proper container management

echo "Starting AWS Log Checker Helper as web application..."
echo "This will be accessible at http://localhost:8080"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Stop and remove any existing container with the same name
if docker ps -a --format '{{.Names}}' | grep -q "^aws-log-helper$"; then
    echo "Stopping existing container..."
    docker stop aws-log-helper > /dev/null 2>&1
    echo "Removing existing container..."
    docker rm aws-log-helper > /dev/null 2>&1
fi

# Create local data directory if it doesn't exist
DATA_DIR="$(pwd)/docker-data"
if [ ! -d "$DATA_DIR" ]; then
    echo "Creating persistent data directory: $DATA_DIR"
    mkdir -p "$DATA_DIR"
fi

# Build the container
echo "Building Docker container..."
docker build -t helperapp-aws-log-helper .

echo "Starting web server with persistent data storage..."
echo "Data will be stored in: $DATA_DIR"
echo ""
echo "🌐 Open your browser to: http://localhost:8080"
echo "📊 Press Ctrl+C to stop the application"
echo ""

# Run the container with absolute path volume mounting for persistent storage
docker run --rm -it \
    -p 8080:8080 \
    -v "$DATA_DIR":/home/appuser/app/data \
    --name aws-log-helper \
    helperapp-aws-log-helper

echo ""
echo "Application has stopped."
echo "Your data is safely stored in: $DATA_DIR"