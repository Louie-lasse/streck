#!/bin/bash
# startup.sh - Run the Streck Bot and then launch the browser

# Change to the working directory where your Python script is located
cd /path/to/your/streck || { echo "Failed to change directory"; exit 1; }

# Ensure that the network connection has been established
sleep 2

# Launch the Python script in a terminal window.
lxterminal -e "bash -c 'python3 /path/to/startup_script.py; exec bash'" &

# Wait a few seconds to ensure the Python script is up and the network is ready
sleep 5

chromium-browser --start-fullscreen --force-device-scale-factor=0.9 http://localhost:5000 &
