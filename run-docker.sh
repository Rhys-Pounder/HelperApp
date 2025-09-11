#!/bin/bash

# --- OS Detection and Setup ---
if [ "$(uname)" == "Darwin" ]; then
    # --- macOS Setup ---
    echo "macOS detected. Configuring for XQuartz."
    
    # Set the DISPLAY variable for the host shell, so xhost can find the server.
    # This is the crucial missing step.
    export DISPLAY=:0
    
    # Get your Mac's local IP address
    IP_ADDRESS=$(ipconfig getifaddr en0)
    
    echo "Authorizing IP: $IP_ADDRESS"
    # Use the full path to the xhost command provided by XQuartz
    /opt/X11/bin/xhost + "$IP_ADDRESS"
    
    # Set the DISPLAY variable for inside the container
    DISPLAY_CONFIG_FOR_CONTAINER="$IP_ADDRESS:0"
    DOCKER_ARGS="-e DISPLAY=$DISPLAY_CONFIG_FOR_CONTAINER"

elif [ "$(uname)" == "Linux" ]; then
    # --- Linux Setup ---
    echo "Linux detected. Configuring for X11."
    xhost +local:
    DOCKER_ARGS="-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY"

else
    echo "Unsupported OS: $(uname)"
    exit 1
fi

# --- Run the Docker Container ---
echo "Starting Docker container..."
docker run --rm -it $DOCKER_ARGS helperapp-aws-log-helper

# --- Cleanup ---
# Revoke the permission after the container exits
if [ "$(uname)" == "Darwin" ]; then
    echo "Revoking IP authorization."
    # Use the full path here as well
    /opt/X11/bin/xhost - "$IP_ADDRESS"
elif [ "$(uname)" == "Linux" ]; then
    xhost -local:
fi