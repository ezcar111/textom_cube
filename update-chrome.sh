#!/bin/bash

cd /usr/local/bin
LATEST_RELEASE=`curl http://chromedriver.storage.googleapis.com/LATEST_RELEASE`

VERSION=`uname -p`

if [ "$VERSION" = "x86_64" ]; then
  WEBDRIVER_PATH="http://chromedriver.storage.googleapis.com/$LATEST_RELEASE/chromedriver_linux64.zip"
else
  WEBDRIVER_PATH="http://chromedriver.storage.googleapis.com/$LATEST_RELEASE/chromedriver_linux32.zip"
fi

echo $WEBDRIVER_PATH
wget $WEBDRIVER_PATH

apt install unzip
unzip -o chromedriver_linux64.zip
rm chromedriver_linux64.zip

wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
apt-get update -y
apt-get install google-chrome-stable
