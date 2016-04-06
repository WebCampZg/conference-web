# Webcamp Zagreb conference web

[![Build Status](https://circleci.com/gh/WebCampZg/conference-web.svg?style=svg)](https://circleci.com/gh/WebCampZg/conference-web)


## Dev env setup

### The Vagrant option

First install Vagrant and Ansible:

http://docs.vagrantup.com/v2/installation/
http://docs.ansible.com/intro_installation.html#installing-the-control-machine

Create the workspace and clone the web and devops repo

    mkdir webcamp && cd webcamp
    git clone https://github.com/WebCampZg/devops
    git clone https://github.com/WebCampZg/conference-web

Enter the conference-web folder (where the Vagrantfile is located)
and provision the VM.

    cd conference-web
    vagrant up --provision

`NOTE`: The Vagrantfile exposes port 8000 on you local machine,
if this is port is already taken vagrant will fail to bring up the machine


Once the provisioning is done you should have everything set up and can
ssh to the VM.

    vagrant ssh

And run the development server:

    cd app
    ./devserver.sh

`NOTE`: The devserver will start up and you can visit the app on your local machine
on `http://localhost:8000`.

### The Docker way

First install Docker and Docker-Compose

https://docs.docker.com/compose/install/

Start the db and web containers using the following command:

    make run

The django devserver should be running and you should be able to visit the app
on your host machine on `http://localhost:8000` (or some IP on a mac).

You might want to run the database migrations, using the following command (after the above command is done):

    make migrate

`NOTE`: Compose uses the port 8000 to attach the app to. If that port is already taken
by some other process it will fail.

