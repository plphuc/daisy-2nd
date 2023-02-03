#!/bin/sh

npm install -g heroku

# Install git
#apt-get update
#apt-get install software-properties-common
#apt-add-repository ppa:git-core/ppa
#apt-get update
#apt-get install git

echo deb http://deb.debian.org/debian buster-backports main | tee /etc/apt/sources.list.d/buster-backports.list
apt update
apt install -t buster-backports git -y
git --version

git config --global user.email "jayhuynh239@gmail.com"
git config --global user.name "Jay Huynh"
