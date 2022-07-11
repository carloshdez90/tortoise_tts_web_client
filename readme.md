# Getting Started
- clone this repo
- update submodule 
    - ```git submodule init```
    - ```git submodule update```

# Setup google service account to use google bucket
- put json file into api folder

# Fill dotenv file in helper folder
- Use the ```.env.example``` as template

# Install dependencies
```bash
pip install -r requirements.txt
```

# Install TorToiSe-TTS
- https://github.com/neonbjb/tortoise-tts#local-installation 

# Run API - development mode
- Move to api folder (api project) and run
```bash
uvicorn main:app --reload
```

# Create base image, using lambda-stack
- https://lambdalabs.com/lambda-stack-deep-learning-software 
- https://github.com/lambdal/lambda-stack-dockerfiles

## Download pytorch in repo root folder
- ```wget https://download.pytorch.org/whl/cu113/torch-1.11.0%2Bcu113-cp38-cp38-linux_x86_64.whl```
## Build base image
- move to docker-lambda folder
- then, build de image ```sudo docker build -t lambda-stack:20.04 -f Dockerfile.focal .```
- Use this image to build your custom image with your code.

## Create custom image based on lambda-stack
- ```docker build --no-cache -t tts-generator:v1 .```

## Run docker-compose as a service
- run the following script as root
```bash
    #!/bin/bash
    # Create a systemd service that autostarts & manages a docker-compose instance in the current directory
    # by Uli Köhler - https://techoverflow.net
    # https://techoverflow.net/2020/10/24/create-a-systemd-service-for-your-docker-compose-project-in-10-seconds/
    # Licensed as CC0 1.0 Universal
    SERVICENAME=$(basename $(pwd))
    echo "Creating systemd service... /etc/systemd/system/${SERVICENAME}.service"
    # Create systemd service file
    sudo cat >/etc/systemd/system/$SERVICENAME.service <<EOF
    [Unit]
    Description=$SERVICENAME
    Requires=docker.service
    After=docker.service
    [Service]
    Restart=always
    User=root
    Group=docker
    WorkingDirectory=$(pwd)
    # Shutdown container (if running) when unit is started
    ExecStartPre=$(which docker-compose) -f docker-compose.yaml down
    # Start container when unit is started
    ExecStart=$(which docker-compose) -f docker-compose.yaml up
    # Stop container when unit is stopped
    ExecStop=$(which docker-compose) -f docker-compose.yaml down
    [Install]
    WantedBy=multi-user.target
    EOF
    echo "Enabling & starting $SERVICENAME"
    # Autostart systemd service
    sudo systemctl enable $SERVICENAME.service
    # Start systemd service now
    sudo systemctl start $SERVICENAME.service
```
