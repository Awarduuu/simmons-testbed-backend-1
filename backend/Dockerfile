FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev \
    build-essential libssl-dev libffi-dev python3-setuptools 

WORKDIR /app
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt

RUN apt-get install -y ffmpeg
RUN apt-get install libsndfile1 -y

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade Pillow
RUN pip3 install markupsafe==1.0.0
RUN pip3 install -r requirements.txt 
