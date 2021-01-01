# Base layer stuff.
FROM python:slim-buster

RUN apt update && apt install ssh rsync -y

# User stuff.
RUN useradd -m zsync

RUN mkdir -p /home/zsync/.ssh

RUN chown -R zsync:zsync /home/zsync/.ssh

WORKDIR /home/zsync

# Code stuff.
COPY zsync.py .

COPY requirements.txt .

COPY retrieve-key.sh .

# Python packages installation.
RUN pip3 install -r requirements.txt

# Final user stuff.
USER zsync

# Init cmd.
CMD ["python3", "zsync.py"]