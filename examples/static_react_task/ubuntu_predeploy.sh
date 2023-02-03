#!/bin/sh

pip install --upgrade pip
pip install -e .

mephisto check

yarn install
yarn build-all

npm install -g heroku

