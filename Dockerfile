FROM python:3.8.12-slim-bullseye

# RUN apt-get update && apt-get install -y build-essential libssl-dev libffi-dev python-dev

# Define working directory
WORKDIR /opt/app

# Exposing ports in container
EXPOSE 5000

# Copy requirements for pip
COPY requirements.txt .

# Run the requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy source code in container
COPY . .

# Run the python server
CMD ./entrypoint.sh
