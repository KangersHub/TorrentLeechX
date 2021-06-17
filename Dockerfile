FROM ghcr.io/amirulandalib/torrentleechx:latest

WORKDIR /app

COPY . .

RUN  chmod +x extract
