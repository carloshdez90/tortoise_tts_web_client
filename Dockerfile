FROM lambda-stack:20.04

#Install dependencies
RUN apt update && apt install python3.8-venv libsndfile1 -y

#Create virtual env
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /code

#Copying TorToiSe-TTS code
COPY tortoise-tts/ /code/tortoise-tts/

#Copying app code
COPY api/ /code/api/

COPY requirements.txt /code/

# Install pythorch with cudnn support
COPY torch-1.11.0+cu113-cp38-cp38-linux_x86_64.whl /code/

RUN pip install torch-1.11.0+cu113-cp38-cp38-linux_x86_64.whl && \ 
    pip install torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113 && \
    pip install --no-cache-dir --upgrade -r requirements.txt

# Install TorToiSe-TTS locally (inside the container)
RUN cd tortoise-tts && python setup.py install 

WORKDIR /code/api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers", "--workers", "4"]