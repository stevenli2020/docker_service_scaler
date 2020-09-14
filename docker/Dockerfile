FROM ubuntu:18.04
MAINTAINER steven <devteamsbox@gmail.com>

RUN apt update && apt install -y nano curl net-tools python2.7 netcat
RUN cp /usr/bin/python2.7 /usr/bin/python
RUN curl -fsSL https://get.docker.com | sh
# apt update && apt install -y nano curl net-tools python2.7 netcat && cp /usr/bin/python2.7 /usr/bin/python && curl -fsSL https://get.docker.com | sh
RUN apt-get clean && apt-get autoremove --purge
COPY ./conf /conf
COPY ./app /app
RUN chmod +x /app/run.py
WORKDIR /app

EXPOSE 733
CMD ["/app/run.py"]
