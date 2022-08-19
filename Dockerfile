FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime

#Install dependencies
RUN apt update && apt install python3.8-venv libsndfile1 -y

WORKDIR /app

COPY . /app/

RUN pip install torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113 && \
    pip install --no-cache-dir --upgrade -r requirements.txt 

# Install TorToiSe-TTS locally (inside the container)
RUN cd tortoise-tts && python setup.py install 

WORKDIR /app/api

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers", "--workers", "4"]
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:80", "--workers", "4", "--keep-alive", "7200", "-t", "7200"]
