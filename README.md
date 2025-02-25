# streck

This application is an extention of [Streck](https://github.com/urdh/streck.git). For more details, visit the original repo. This repo also includes `Streck` but with the addition of `Bastugatan`.

# Bastugatan

Bastugatan is an application built to work in parallel with `streck`. To use it, you need to populate an `.env` file with values, and add `slack_id` to the db entry which will be the admin.

To find your slack_id, simply dm `whoami` to the bot

## Startup script

Included is a startup script for the application. This will start the full application on boot (assuming the below steps are followed). Every day at 12:00 the script will

1. Make a backup of the database, for a maximum of 14. Older backups are removed
2. Check if any application has crashed, if so: restart it.
3. Check for updates on the detailed branch. If updates are present, pull them and restart the application

## Setting up the service

### Move startup_script.py

Move the script to any location to prevent conflicts if the script is updated.

### Simple startup setup

For a raspberry PI, modify `~/.config/lxsession/LXDE-pi/autostart`, adding the content:

```conf
@lxterminal --working-directory=/path/to/your/streck --command="bash -c 'sleep 5; python3 /path/to/startup_script.py'"
@bash -c "sleep 5; chromium-browser --start-fullscreen --force-device-scale-factor=0.9 http://localhost:5000"
```

where `/path/to/your/streck` is the location of the streck directory (e.g. `/home/pi/streck`) and `/path/to/startup_script.py` is the path to the script (that has been moved out of the streck directory. e.g. `/home/pi/startup_script.py`)

This is the prefered approach, as the service below has some issues. If you want to work them out you are free to.

### Create the service

Create `/etc/systemd/system/streck-bot.service` with the contents
```ini
[Unit]
Description=Streck Bot with Browser
After=network.target

[Service]
ExecStart=/usr/bin/python3 /new/path/to/startup_script.py
ExecStartPost=/usr/bin/chromium-browser --start-fullscreen --force-device-scale-factor=0.9 http://localhost:5000
WorkingDirectory=/path/to/your/streck
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
where
1. `/new/path/to/startup_script.py` is where the script is placed
2. `/usr/bin/chromium-browser` is (assumed) to be your browser
3. `/path/to/your/streck` is the directory where `streck` is located. The startup script need to be running here to function.

After creating the service, start it with
```zsh
sudo systemctl daemon-reload      # Reload systemd after adding a new service
sudo systemctl enable streck-bot  # Enable the service to start on boot
sudo systemctl start streck-bot   # Start the service manually now
```

You can then use
```zsh
sudo systemctl status streck-bot
```
to check if the service is running. Note that this was built for a raspberry pi being reguralry restarted (~8 times per year). Thus, long term memmory loss due to zombies has not been investigated.

### Usage

Either have the program listen to `main`/`master`, or create a seperate branch for the program to listen to
