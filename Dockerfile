FROM python:alpine

#define working directory
WORKDIR /app

#exposing ports in container
EXPOSE 5000 80

#copy requirements for pip
COPY requirements.txt . 

#get execute permission to entrypoint file
RUN chmod +x ./entrypoint.sh

#run the requirements
RUN pip install -U pip \
    pip install -r requirements.txt

#copy source code in container
COPY . .

#run the python server
CMD ["bash", "-c", "./entrypoint.sh"]
