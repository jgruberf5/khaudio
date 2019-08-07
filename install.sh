#!/bin/bash

# add packages required to run clients
/bin/bash ./pacakages/install.sh

# add the needed sound modules
cp -f ./kernel_modules/modules /etc/modules
cp ./kernel_modules/modprobe.d/sound.conf /etc/modprobe.d/sound.conf
modprobe snd-aloop
modprobe snd-dummy

# add sound device configurations and effects processing
cp ./alsa/asound.conf /etc/asound.conf
cp ./alsa/asound.state /var/lib/alsa/asound.state
alsactl restore
alsactl nrestore

# add patching service from USB input to effect processors
cp ./alsaloop/config/alsaloop.conf /etc/alsaloop.conf
cp ./alsaloop/systemd/alsaloop.service /lib/systemd/system/alsaloop.service
systemctl enable alsaloop.service
systemclt alsaloop start

# add KHConf SIP client service scripts and template configuration
mkdir -p /var/lib/khconf
cp ./khconf/scripts/* /var/lib/khconf/
chmod +x /var/lib/khconf/*
mkdir -p /var/lib/khconf/config
cp ./khconf/config/template.conf /var/lib/khconf/config/template.conf

# add KHStreamer client service scripts and template configuration
mkdir -p /var/lib/khstreamer
cp ./khstreamer/scripts/* /var/lib/khstreamer/
chmod +x /var/lib/khstreamer/*
mkdir -p /var/lib/khstreamer/config
cp ./khstreamer/config/template.conf /var/lib/khstreamer/config/template.conf

# add meeting scheduler service
