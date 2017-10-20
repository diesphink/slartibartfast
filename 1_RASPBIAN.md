# Install raspbian and basic setup
Based on this [guide](https://www.filipeflop.com/blog/como-conectar-display-lcd-tft-raspberry-pi/), this [answer](https://raspberrypi.stackexchange.com/a/66424) on raspberrypi stackexchange and this [post](https://www.raspberrypi.org/forums/viewtopic.php?t=66184) on raspberrypi.org forums.
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
