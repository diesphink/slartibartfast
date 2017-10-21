# Install raspbian and basic setup

### Install image
Download octopi from [octoprint.org](https://octopi.octoprint.org/).

### Configure wifi
Edit file `/boot/octopi-network.txt` with network information

You can now boot your raspberry pi.

### Change default password

The default login on pi is pi/raspberry, and you **really** should change that.

### Update system
Connect to wifi then upgrade system:
```
sudo apt-get update
sudo apt-get dist-upgrade
```
and then reboot.
