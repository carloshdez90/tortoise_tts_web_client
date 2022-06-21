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

## Download pytorch
- ```wget https://download.pytorch.org/whl/cu113/torch-1.11.0%2Bcu113-cp38-cp38-linux_x86_64.whl```
## Build base image
- move to docker-lambda folder
- then, build de image ```sudo docker build -t lambda-stack:20.04 -f Dockerfile.focal .```
- Use this image to build your custom image with your code.

## Create custom image based on lambda-stack
- ```docker build -t tts-generator:v1 .```