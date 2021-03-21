FROM ubuntu:latest
MAINTAINER Pugachev Alexander


#RUN adduser --disabled-password --gecos "" username && su username
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python3.6 python3-pip
RUN apt-get install -y curl

#RUN curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.11.2-linux-x86_64.tar.gz
#RUN tar -xvf elasticsearch-7.11.2-linux-x86_64.tar.gz
#RUN cd elasticsearch-7.11.2/bin
#RUN ./elasticsearch

COPY . /ingredients2recipe
WORKDIR ingredients2recipe

RUN pip3 install -r requirements.txt