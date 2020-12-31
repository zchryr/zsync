FROM python:slim-buster

RUN apt update && apt install ssh jq rsync -y

RUN useradd -m replication

RUN mkdir -p /home/replication/.ssh

RUN chown -R replication:replication /home/replication/.ssh

WORKDIR /home/replication

COPY . .

USER replication

CMD ["python3", "replication.py"]