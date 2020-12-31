# Base layer stuff.
FROM python:slim-buster

RUN apt update && apt install ssh jq rsync -y

# User stuff.
RUN useradd -m replication

RUN mkdir -p /home/replication/.ssh

RUN chown -R replication:replication /home/replication/.ssh

WORKDIR /home/replication

# Code stuff.
COPY replication.py .

COPY requirements.txt .

COPY retrieve-key.sh .

# Python packages installation.
RUN pip3 install -r requirements.txt

# Final user stuff.
USER replication

# Init cmd.
CMD ["python3", "replication.py"]