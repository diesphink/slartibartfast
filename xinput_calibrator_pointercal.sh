#!/bin/sh

# script to make the changes permanent (xinput is called with every Xorg start)
#
# can be used from Xsession.d
# script needs tee and sed (busybox variants are enough)
#
# original script: Martin Jansa <Martin.Jansa@gmail.com>, 2010-01-31
# updated by Tias Guns <tias@ulyssis.org>, 2010-02-15
# updated by Koen Kooi <koen@dominion.thruhere.net>, 2012-02-28

# Downloaded from http://ozzmaker.com/piscreen/xinput_calibrator_pointercal.sh on 2017-10-20.

PATH="/usr/bin:$PATH"

BINARY="xinput_calibrator"
CALFILE="/etc/pointercal.xinput"
LOGFILE="/var/log/xinput_calibrator.pointercal.log"

if [ -e $CALFILE ] ; then
  if grep replace $CALFILE ; then
    echo "Empty calibration file found, removing it"
    rm $CALFILE
  else
    echo "Using calibration data stored in $CALFILE"
    . $CALFILE && exit 0
  fi
fi

CALDATA=`xinput_calibrator --output-type xinput -v | grep '    xinput set' | sed 's/^    //g; s/$/;/g'`
if [ ! -z "$CALDATA" ] ; then
  echo $CALDATA > $CALFILE
  echo "Calibration data stored in $CALFILE (log in $LOGFILE)"
fi
