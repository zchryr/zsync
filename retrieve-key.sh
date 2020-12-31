#! /bin/bash

remoteip=$(jq .remoteip args.json)

remoteip=$(echo "$remoteip" | tr -d '"')

ssh-keyscan $remoteip >> /home/replication/.ssh/known_hosts