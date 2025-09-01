#!/bin/bash
# startup.sh - Run the Streck Bot and then launch the browser

# Change to the working directory where your Python script is located
cd /path/to/your/streck || { echo "Failed to change directory"; exit 1; }

lxterminal -e "bash -c 'python streck.py; exec bash'" &

echo "Waiting for network connection..."
for i in {1..30}; do
    if ping -c 1 -W 1 8.8.8.8 &> /dev/null; then
        echo "Network connected!"
        break
    fi
    echo "Still waiting for network... ($i)"
    sleep 1
done

lxterminal -e "bash -c 'python3 bastugatan.py; exec bash'" &

echo "Waiting for scripts to start..."
for i in {1..15}; do
    if curl -s --connect-timeout 1 http://localhost:5000 &> /dev/null; then
        echo "Server is up!"
        break
    fi
    echo "Still waiting for server... ($i)"
    sleep 1
done

xdotool mousemove 9999 9999 || echo "Failed to move mouse"

chromium-browser --start-fullscreen --incognito --force-device-scale-factor=0.9 http://localhost:5000
