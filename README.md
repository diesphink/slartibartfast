# slartibartfast
Configuração do raspberry pi + octoprint

# Install raspbian and TFT LCD Configuration
Based on this [guide](https://www.filipeflop.com/blog/como-conectar-display-lcd-tft-raspberry-pi/).
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
Edit `/boot/config.txt`, appending:

```
dtoverlay=piscreen,speed=16000000,rotate=90
```
and then reboot.

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
cd ~
wget https://raw.githubusercontent.com/diesphink/slartibartfast/master/xinput_calibrator_pointercal.sh
sudo cp ~/xinput_calibrator_pointercal.sh /etc/X11/Xsession.d/xinput_calibrator_pointercal.sh
```

Append to `/etc/xdg/lxsession/LXDE-pi/autostart`:
```
sudo /bin/sh /etc/X11/Xsession.d/xinput_calibrator_pointercal.sh
```

### Fix inverted touch
Based on [this post](https://raspberrypi.stackexchange.com/questions/60872/inverted-gpio-touchscreen-using-99-calibration-conf).

Download and install overlay from [waveshare-dtoverlays (github)](https://github.com/swkim01/waveshare-dtoverlays)
```
wget https://github.com/swkim01/waveshare-dtoverlays/raw/master/waveshare35a-overlay.dtb
sudo cp waveshare35a-overlay.dtb /boot/overlays/
```

Edit `/boot/config.ini`, appending:
```
dtoverlay=waveshare35a:rotate=270,swapxy=1
```

And then reboot.

### Fix inverted touch on callibration
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
To start x on the TFT display, run:
```
FRAMEBUFFER=/dev/fb1 startx
```

### Auto start on TFT display
TBD.

