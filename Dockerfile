FROM ubuntu:18.04


RUN mkdir ./app
RUN chmod 777 ./app
WORKDIR ./app
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN apt -qq update
RUN apt -qq install -y python3 python3-pip
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash","start.sh"]
