# start with a base image
FROM ubuntu:latest

MAINTAINER Real Python <info@realpython.com>

# initial update
RUN apt-get update -q

# install wget, java, curl and mini-httpd web server
RUN apt-get install -yq wget default-jre-headless  mini-httpd curl

# install elasticsearch
RUN cd /tmp && \
    wget -nv https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.2.0-linux-x86_64.tar.gz && \
    tar zxf elasticsearch-7.2.0-linux-x86_64.tar.gz && \
    rm -f elasticsearch-7.2.0-linux-x86_64.tar.gz && \
    mv /tmp/elasticsearch-7.2.0 /elasticsearch

# install kibana
RUN cd /tmp && \
    curl -O https://artifacts.elastic.co/downloads/kibana/kibana-7.8.0-linux-x86_64.tar.gz && \
    tar -xzf kibana-7.8.0-linux-x86_64.tar.gz && \
    rm -rf kibana-7.8.0-linux-x86_64.tar.gz && \
    mv /tmp/kibana-7.8.0-linux-x86_64 /kibana

# expose ports
EXPOSE 8000 9200

# start elasticsearch
CMD /elasticsearch/bin/elasticsearch -Des.logger.level=OFF & mini-httpd -d /kibana -h `hostname` -r -D -p 8000
