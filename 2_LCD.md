# Configure LCD
Based on this [guide](https://github.com/BillyBlaze/OctoPrint-TouchUI/wiki/Setup:-Boot-to-Browser-(OctoPi-or-Jessie-Light)), this other [guide](https://www.filipeflop.com/blog/como-conectar-display-lcd-tft-raspberry-pi/), this [answer](https://raspberrypi.stackexchange.com/a/66424) on raspberrypi stackexchange and this [post](https://www.raspberrypi.org/forums/viewtopic.php?t=66184) on raspberrypi.org forums.

### Enable drivers
Install dependencies and needed programs:
```
sudo apt-get install --no-install-recommends xinit xinput xserver-xorg xserver-xorg-video-fbdev x11-xserver-utils matchbox unclutter chromium-browser
```
Download and install overlay from [waveshare-dtoverlays (github)](https://github.com/swkim01/waveshare-dtoverlays)
```
git clone https://github.com/swkim01/waveshare-dtoverlays.git
sudo cp waveshare-dtoverlays/waveshare35a-overlay.dtb /boot/overlays/
```

Edit `/boot/config.txt`, appending:
```
dtoverlay=waveshare35a:rotate=270,swapxy=0
```

Create file `/usr/share/X11/xorg.conf.d/99-fbdev.conf`, with:
```
Section "Device"
  Identifier "touchscreen"
  Driver "fbdev"
  Option "fbdev" "/dev/fb1"
EndSection
```

And then reboot.

### Install TouchUI to launch on boot

Download needed files:
```
git clone https://github.com/BillyBlaze/OctoPrint-TouchUI-autostart.git ~/TouchUI-autostart/		
```

Copy service file and register it as auto boot:
```
sudo cp ~/TouchUI-autostart/touchui.init /etc/init.d/touchui
sudo chmod +x /etc/init.d/touchui
sudo cp ~/TouchUI-autostart/touchui.default /etc/default/touchui
sudo update-rc.d touchui defaults
```

### Callibration

Stop TouchUI:

```
sudo service touchui stop
```

Install xinput-calibrator:
```
curl -sLS https://apt.adafruit.com/add | sudo bash
sudo apt-get install -y xinput-calibrator

```

Calibrate:
```
sudo xinit ~/TouchUI-autostart/calibration.xinit
```

Copy Section until Endsection into `/etc/X11/xorg.conf.d/99-calibration.conf`


### Fix inverted touchscreen
Edit `/usr/share/X11/xorg.conf.d/40-libinput.conf`, adding the highlighted line:
<pre>
Section "InputClass"
    Identifier "libinput touchscreen catchall"
    MatchIsTouchScreen "on"
    MacthDevicePath "/dev/input/event*"
    Driver "libinput"
    <b>Option "TransformationMatrix" "0 1 0 -1 0 1 0 0 1"</b>
EndSection
</pre>


And then reboot.
