FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# INSTALL REQUIRED PACKAGES
RUN apt-get update -y && apt-get install -y python3.9 python3-pip curl wget software-properties-common
RUN apt-add-repository ppa:git-core/ppa
RUN apt-get update -y && apt-get install -y git
RUN pip3 install --upgrade pip

SHELL ["/bin/bash", "--login", "-i", "-c"]
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
RUN source /root/.bashrc && nvm install 15.14.0 && nvm use 15.14.0
ENV PATH="/root/.nvm/versions/node/v15.14.0/bin:${PATH}"
RUN npm install -g npm
RUN npm install -g heroku
RUN npm install -g yarn

# ec2 architect requires `ssh-keygen` util, so we need to install it.
# Firstly, remove `yarn` repo as it causes error that stops building a container. Error:
# (Error: The repository 'https://dl.yarnpkg.com/debian stable InRelease' is not signed)
RUN rm /etc/apt/sources.list.d/yarn.list
RUN apt update
RUN apt install keychain -y

COPY . /mephisto
RUN mkdir ~/.mephisto

# Create the main Mephisto data directory
# RUN mkdir /mephisto/data

# Write the mephisto config file manually for now to avoid prompt.
# For bash-style string $ expansion for newlines,
# we need to switch the shell to bash:
SHELL ["/bin/bash", "-c"]
RUN echo $'core: \n  main_data_directory: /mephisto/data' >> ~/.mephisto/config.yml

RUN cd /mephisto && pip3 install -e .

CMD bash -c "sleep infinity"