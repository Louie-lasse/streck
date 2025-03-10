# streck

This application is an extention of [Streck](https://github.com/urdh/streck.git). For more details, visit the original repo. This repo also includes `Streck` but with the addition of `Bastugatan`.

# Bastugatan

Bastugatan is an application built to work in parallel with `streck`. To use it, you need to populate an `.env` file with values, and add `slack_id` to the db entry which will be the admin.

To find your slack_id, simply dm `whoami` to the bot

## How to run

Either, run `streck.py` and `bastugatan.py` for streck and bastugatan respectively. Alternatively, you can run the `startup_script.py`

## Startup script

Included is a startup script for the application. This will start the full application on boot (assuming the below steps are followed). Every day at 12:00 the script will

1. Make a backup of the database, for a maximum of 14. Older backups are removed
2. Check if any application has crashed, if so: restart it.
3. Check for updates on the detailed branch. If updates are present, pull them and restart the application

## Setting up the service

### Copy scripts

Copy the python script `startup_script.py` to any location to prevent conflicts if the script is updated. Also copy the shell script `bastugatan.sh` (note: not `bastugatan.py`).

### Simple startup setup

For a raspberry PI, modify `~/.config/lxsession/LXDE-pi/autostart`, adding the content:

```conf
@lxterminal -e /home/pi/bastugatan/script/location
```

where `/home/pi/bastugatan/script/location` is the location of shell script (e.g. `/home/pi/bastugatan.sh`).

Also, the tool `xdotool` needs installation

```sh
sudo apt-get install xdotool
```

#### Enable/disable

To enable the application on startup, run `chmod +x /path/to/bastugatan.sh`. To disable it, run `chmod -x /path/to/bastugatan.sh`.

#### Modify networks

If the device running the service changes location/network, default networks may need to be configured. To do this, edit `/etc/wpa_supplicant/wpa_supplicant.conf` and add `priority=n` to each, where `n` is order of priority with highest priority being `1`.

### Usage

Either have the program listen to `main`/`master`, or create a seperate branch for the program to listen to
