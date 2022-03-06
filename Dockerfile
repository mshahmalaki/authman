FROM python:3.8.12-slim-bullseye

# RUN apt-get update && apt-get install -y build-essential libssl-dev libffi-dev python-dev

# Define user and switch
RUN useradd -ms /bin/bash myuser
USER myuser

# Define working directory
WORKDIR /home/myuser

# Exposing ports in container
EXPOSE 5000

# Copy requirements for pip
COPY --chown=myuser:myuser requirements.txt .

# Run the requirements
RUN pip install --upgrade pip
RUN pip install --user -r requirements.txt

# Copy source code in container
COPY --chown=myuser:myuser . .

# Run the python server
CMD ./entrypoint.sh
