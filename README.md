# AWS Log Checker Helper Application

A Python GUI application that reminds users every 2 hours to check AWS logs and provides a convenient interface to log check results with persistent storage. Built to be run seamlessly on both **macOS** and **Linux** using Docker.



## Features

-   **Cross-Platform with Docker**: A single script provides a native experience on both macOS and Linux.
-   **Automatic Reminders**: Get reminded every 2 hours to check AWS logs.
-   **User-Friendly GUI**: Clean, tabbed interface built with tkinter.
-   **Data Entry Form**: Log check results with timestamp, outcome, and notes.
-   **Persistent Storage**: SQLite database stores all check records locally on your machine.
-   **Check History**: View and review previous log checks.
-   **Snooze Functionality**: Snooze reminders for 10 minutes.

***

## Getting Started with Docker (Recommended)

This method packages the application and its dependencies into a container, providing the most reliable and consistent experience.

### 1. Prerequisites

First, you'll need to install the necessary tools for your operating system.

#### For macOS 🍏

1.  **Install Docker Desktop**: Download and install from the [official Docker website](https://www.docker.com/products/docker-desktop/).
2.  **Install XQuartz**: This allows your Mac to display graphical applications from the container. The easiest way is using [Homebrew](https://brew.sh/):
    ```bash
    brew install --cask xquartz
    ```
3.  **Configure XQuartz**:
    * Run the **XQuartz** application.
    * Go to **XQuartz > Settings > Security**.
    * Ensure **"Allow connections from network clients"** is checked.
    * Restart XQuartz after changing the setting.

#### For Linux (Ubuntu/Debian) 🐧

1.  **Install Docker Engine**: Follow the official guide to install Docker for your distribution. For Ubuntu, you can find the instructions [here](https://docs.docker.com/engine/install/ubuntu/).
2.  **Install `x11-xserver-utils`** (if not already present): This provides the `xhost` utility needed for display permissions.
    ```bash
    sudo apt-get update && sudo apt-get install x11-xserver-utils
    ```

---

### 2. Installation and Usage

Once the prerequisites are installed, running the application is simple.

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/Rhys-Pounder/HelperApp.git](https://github.com/Rhys-Pounder/HelperApp.git)
    cd HelperApp
    ```

2.  **Build the Docker Image**:
    ```bash
    docker build -t helperapp-aws-log-helper .
    ```

3.  **Run the Application**:
    Execute the provided run script. It will automatically detect your OS and configure the display settings.
    ```bash
    ./run-docker.sh
    ```

The application GUI should now appear on your screen! The `run-docker.sh` script handles all the platform-specific logic for you.

<details>
<summary>Click to see the contents of <code>run-docker.sh</code></summary>

```bash
#!/bin/bash

# --- OS Detection and Setup ---
if [ "$(uname)" == "Darwin" ]; then
    # --- macOS Setup ---
    echo "macOS detected. Configuring for XQuartz."
    export DISPLAY=:0
    IP_ADDRESS=$(ipconfig getifaddr en0)
    
    echo "Authorizing IP: $IP_ADDRESS"
    /opt/X11/bin/xhost + "$IP_ADDRESS"
    
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
if [ "$(uname)" == "Darwin" ]; then
    echo "Revoking IP authorization."
    /opt/X11/bin/xhost - "$IP_ADDRESS"
elif [ "$(uname)" == "Linux" ]; then
    xhost -local:
fi
```
</details>

***

## Application Usage Guide

The application has three main tabs:

#### 1. Log Check Tab
-   Enter the date and time of your check (click "Now" for current time).
-   Select an outcome from the dropdown menu.
-   Add any relevant notes.
-   Click "Save Check" to store the record.

#### 2. History Tab
-   View all previous check records.
-   Double-click any record to see full details.
-   Click "Refresh" to update the list.

#### 3. Settings Tab
-   Start/Stop automatic reminders.
-   Test the reminder system.
-   View application information.

***

## Troubleshooting

#### On macOS: Error `couldn't connect to display` or `Authorization required`
-   **Is XQuartz Running?**: Make sure the XQuartz application is open before you run the script.
-   **Security Settings**: Double-check that **"Allow connections from network clients"** is enabled in XQuartz settings. You may need to restart XQuartz or log out/in again for it to take effect.
-   **Firewall**: Ensure your firewall is not blocking the connection from Docker.

#### On Linux: Error `cannot open display`
-   **Permissions**: The `xhost +local:` command in the script should handle this, but ensure you are running the script as a user with an active graphical session.

#### Docker Errors
-   **`docker` command not found**: Ensure Docker is installed and its daemon is running. On Linux, you may need to add your user to the `docker` group to run commands without `sudo`.
-   **Image not found**: Make sure you have successfully run the `docker build -t helperapp-aws-log-helper .` command from within the project directory.

***

## Configuration

Edit `config.py` to customize:
-   Reminder interval (default: 2 hours)
-   Snooze duration (default: 10 minutes)
-   Database location (Note: Data is stored on the host, not in the container).

<br>

<details>
<summary><h3>Running Locally (Alternative method without Docker)</h3></summary>

### Requirements
- Python 3.6 or higher
- `tkinter`

### Installation

1.  Clone this repository:
    ```bash
    git clone [https://github.com/Rhys-Pounder/HelperApp.git](https://github.com/Rhys-Pounder/HelperApp.git)
    cd HelperApp
    ```

2.  Ensure tkinter is installed:
    -   On **Ubuntu/Debian**: `sudo apt update && sudo apt install python3-tk`
    -   On **macOS**: `tkinter` is typically included with Python installations from python.org.

3.  Run the application:
    ```bash
    python3 main.py
    ```
</details>