#!/bin/sh

rm -rf node_modules
rm package-lock.json
current_dir=$(pwd)

# Install all dependencies
cd /mephisto
yarn install
yarn build-all

# Link the annotator-tracker package
cd /mephisto/packages/annotated/annotator-tracker
npm link

cd $current_dir
npm link @annotated/annotator-tracker
npm install
