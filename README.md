# Install raspbian and TFT LCD Configuration
Based on this [guide](https://www.filipeflop.com/blog/como-conectar-display-lcd-tft-raspberry-pi/) and [this answer on raspberrypi stackexchange](https://raspberrypi.stackexchange.com/a/66424).
### Install image
Download raspbian with desktop image from [raspberrypi.org](https://www.raspberrypi.org/downloads/raspbian/)

### Upgrade system
Connect to wifi then upgrade system:
```
sudo apt-get update
sudo apt-get dist-upgrade
```
and then reboot.

### Enable drivers
Download and install overlay from [waveshare-dtoverlays (github)](https://github.com/swkim01/waveshare-dtoverlays)
```
git clone https://github.com/swkim01/waveshare-dtoverlays.git
sudo cp waveshare-dtoverlays/waveshare35a-overlay.dtb /boot/overlays/
```

Edit `/boot/config.ini`, appending:
```
dtoverlay=waveshare35a:rotate=270,swapxy=1
```

And then reboot.

### Callibration
Edit `/usr/share/X11/xorg.conf.d/99-fbturbo.conf`, commenting out the following line:
```
# Option “fbdev” “/dev/fb0”
```

Install dependencies:
```
sudo apt-get install libtool libx11-dev xinput autoconf libx11-dev libxi-dev x11proto-input-dev -y
```

Download, compile and install xinput_callibrator
```
git clone https://github.com/tias/xinput_calibrator
cd xinput_calibrator/
 ./autogen.sh
make
sudo make install
```

Download and install callibration script:
```
git clone https://github.com/diesphink/slartibartfast.git
sudo cp slartibartfast/xinput_calibrator_pointercal.sh /etc/X11/Xsession.d/xinput_calibrator_pointercal.sh
```

Append to `/etc/xdg/lxsession/LXDE-pi/autostart`:
```
sudo /bin/sh /etc/X11/Xsession.d/xinput_calibrator_pointercal.sh
```

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


### Testing display
To start X on the TFT display, run:
```
FRAMEBUFFER=/dev/fb1 startx
```

### Auto start on TFT display
TBD.
