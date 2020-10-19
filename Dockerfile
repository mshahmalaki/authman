FROM python:slim

#define working directory
WORKDIR /opt/app

#exposing ports in container
EXPOSE 5000

#copy requirements for pip
COPY requirements.txt .
COPY entrypoint.sh .

#get execute permission to entrypoint file
RUN chmod +x ./entrypoint.sh

#run the requirements
RUN pip install --upgrade pip \
    pip install -r requirements.txt

#copy source code in container
COPY . .

#run the python server
CMD ["bash", "-c", "./entrypoint.sh"]
