#! /bin/bash

remoteip=$(jq .remoteip args.json)

remoteip=$(echo "$remoteip" | tr -d '"')

ssh-keyscan $remoteip >> /home/zsync/.ssh/known_hosts