FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev \
    build-essential libssl-dev libffi-dev python3-setuptools 

RUN apt-get install curl -y
RUN apt-get install wget -y
RUN apt-get install sudo -y

RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
RUN apt-get install -y nodejs
RUN apt-get install build-essential

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade Pillow
RUN pip3 install markupsafe==1.0.0
RUN pip3 install -r requirements.txt 

RUN npm install --save ip


