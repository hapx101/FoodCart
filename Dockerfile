FROM ubuntu:latest

RUN apt-get update -y

RUN apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY app/ .

RUN SECRET=`python3 -c 'import secrets; print(secrets.token_hex(32))'`

RUN python3 dbinit.py

ENTRYPOINT [ "flask", "run", "-p", "8080" ]