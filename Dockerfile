FROM ubuntu:latest

WORKDIR /app
RUN chmod 777 /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

RUN apt-get -qq update --fix-missing && \
	apt-get -qq install -y git aria2 wget curl busybox unzip unrar tar python3 ffmpeg python3-pip p7zip-full p7zip-rar locales

RUN curl https://rclone.org/install.sh | bash

RUN mkdir /app/gautam
RUN wget -O /app/gautam/gclone.gz https://git.io/JJMSG && gzip -d /app/gautam/gclone.gz
RUN chmod 0775 /app/gautam/gclone

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt
RUN chmod +x extract

CMD ["bash","start.sh"]
