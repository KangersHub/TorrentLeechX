FROM ubuntu:18.04


RUN mkdir ./app
RUN chmod 777 ./app
WORKDIR ./app

RUN apt -qq update
RUN apt -qq install -y git aria2 wget curl busybox unzip unrar tar python3 python3-pip
RUN wget https://rclone.org/install.sh
RUN bash install.sh

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash","start.sh"]
