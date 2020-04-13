FROM ubuntu:18.04 

RUN apt update 

RUN apt install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY requirements.txt requirements.txt 

RUN pip3 install -r requirements.txt

COPY ./src .
COPY ./test .

RUN mkdir /var/data

ENTRYPOINT ["python3", "main.py"]
