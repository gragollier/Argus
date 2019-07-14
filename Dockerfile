FROM ubuntu:18.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ipmitool python3-pip

WORKDIR /opt/app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./ ./

CMD [ "python3", "monitor.py"]