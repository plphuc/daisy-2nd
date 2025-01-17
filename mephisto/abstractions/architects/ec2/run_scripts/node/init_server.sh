#!/bin/bash

# Copyright (c) Meta Platforms and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


echo "Installing basic requirements..."
# Following is commented out until the aws linux2 repo is no longer lagging
# sudo yum update -y >> /home/ec2-user/routing_server/setup/setup_log.txt 2>&1
sudo yum install -y httpd >> /home/ec2-user/routing_server/setup/setup_log.txt 2>&1

echo "Downloading Node..."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash >> /home/ec2-user/routing_server/setup/setup_log.txt 2>&1
. ~/.nvm/nvm.sh >> /home/ec2-user/routing_server/setup/setup_log.txt 2>&1
nvm install v16.14.2 >> /home/ec2-user/routing_server/setup/setup_log.txt 2>&1

echo "Installing router modules..."
cd /home/ec2-user/routing_server/router/
npm install >> /home/ec2-user/routing_server/setup/setup_log.txt 2>&1

echo "Preparing service..."
sudo cp /home/ec2-user/routing_server/setup/router.service /etc/systemd/system/router.service
sudo chmod 744 /home/ec2-user/routing_server/setup/run_server.sh
sudo chmod 664 /etc/systemd/system/router.service

echo "Launching service..."
sudo systemctl daemon-reload >> /home/ec2-user/routing_server/setup/setup_log.txt 2>&1
sudo systemctl enable router.service >> /home/ec2-user/routing_server/setup/setup_log.txt 2>&1
sudo systemctl start router.service >> /home/ec2-user/routing_server/setup/setup_log.txt 2>&1
