FROM python:slim

#define working directory
WORKDIR /opt/app

#exposing ports in container
EXPOSE 5000

#copy requirements for pip
COPY requirements.txt .

RUN sudo apt-get install build-essential libssl-dev libffi-dev python-dev

#run the requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#copy source code in container
COPY . .

#run the python server
CMD ./entrypoint.sh
