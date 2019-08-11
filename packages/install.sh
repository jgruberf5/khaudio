resumedir=`pwd`

apt update
apt upgrade
apt-get update -oAquire::AllowInsecureRepositories=true
apt-get install deb-multimedia-keyring -oAquire::AllowInsecureRepositories=true
apt-get update
apt-get install lame libfaac-dev libmp3lame-dev libvorbis-dev libopencore-amrwb-dev libtheora-dev libx11-dev libfdk-aac-dev libopencore-amrnb-dev libasound2-dev libasound2-doc libssl-dev alsa-utils swh-plugin tap-plugins csladspa caps python-schedule python-jinja2 python-psutil


cd /usr/src
wget https://www.pjsip.org/release/2.9/pjproject-2.9.tar.bz2
tar -xvjf pjproject-2.9.tar.bz2
cd pjproject-2.9
touch pjlib/include/pj/config_site.h
echo '#define PJMEDIA_AUDIO_DEV_HAS_ALSA      1' >> pjlib/include/pj/config_site.h
echo '#define PJMEDIA_AUDIO_DEV_HAS_PORTAUDIO 0' >> pjlib/include/pj/config_site.h
echo '#define PJMEDIA_HAS_VIDEO       0' >> pjlib/include/pj/config_site.h

touch user.mak
echo "export CFLAGS += -march=armv8-a -mtune=cortex-a53 -mfpu=neon-fp-armv8 -mfloat-abi=hard -mlittle-endian -munaligned-access -ffast-math" >> user.mak
echo "export LDFLGS +=" >> user.mak

./configure
make dep
make

ln -s /usr/src/pjproject-2.9/pjsip-apps/bin/pjsua-armv7l-unknown-linux-gnueabihf /usr/bin/pjsua
chmod +x /usr/bin/pjsua

cd $resumedir
