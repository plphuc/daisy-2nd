#!/bin/sh

pip install --upgrade pip
pip install -e .

mephisto check

yarn install
yarn build-all

npm install -g heroku

git config --global user.email "jayhuynh239@gmail.com"
git config --global user.name "Jay Huynh"
