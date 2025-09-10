#!/bin/bash

# Allow X11 forwarding
xhost +local:docker

# Create data directory if it doesn't exist
mkdir -p ./data

# Run the container
docker compose up --build

# Cleanup X11 permissions
xhost -local:docker