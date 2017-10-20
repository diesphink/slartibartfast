# Install raspbian and basic setup

### Install image
Download raspbian with desktop image from [raspberrypi.org](https://www.raspberrypi.org/downloads/raspbian/)

### Configure wifi and ssh
Add to /boot on SD card an empty file named `ssh`, and a file named `wpa_supplicant.conf` with:
```
country=GB
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="YOUR_SSID"
    psk="YOUR_PASSWORD"
    key_mgmt=WPA-PSK
}
```

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
