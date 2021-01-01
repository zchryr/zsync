# Base layer stuff.
FROM python:slim-buster

RUN apt update && apt install ssh jq rsync -y

# User stuff.
RUN useradd -m sync

RUN mkdir -p /home/sync/.ssh

RUN chown -R sync:sync /home/sync/.ssh

WORKDIR /home/sync

# Code stuff.
COPY sync.py .

COPY requirements.txt .

COPY retrieve-key.sh .

# Python packages installation.
RUN pip3 install -r requirements.txt

# Final user stuff.
USER sync

# Init cmd.
CMD ["python3", "sync.py"]