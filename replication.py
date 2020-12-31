import subprocess
import json
from matterhook import Webhook # https://github.com/numberly/matterhook

# Gets all the json from the args.json file.
argsFile = json.load(open('args.json'))

# Uses 'args.json' to allow Mattermost notifications.
mm = Webhook(argsFile['mmwebhook'].split('hooks')[0][:-1], argsFile['mmwebhook'].split('hooks')[-1][1:])

def mattermostNotification():
    mmattachments = []
    mmmessage = {}
    mmmessage['color'] = '#0ffc03'
    mmmarkdown = '### Title'
    mmmarkdown += 'Line of text\n'
    mmmarkdown += 'stuff'
    mmmarkdown += '''
    | name                               |   date |
    |------------------------------------|--------|
    | Monty Python and the Holy Grail    |   1975 |
    '''

    mmmessage['text'] = mmmarkdown
    mmattachments.append(mmmessage)
    mm.send(attachments=mmattachments)

def remoteSSHKeyRetrieval():
    # Runs a bash script to get the remote key and save it go /home/replication/.ssh/known_hosts.
    subprocess.run(["/bin/bash", "retrieve-key.sh"], capture_output=True)

def rsyncUpload():
    # Checks if user edited the args.json before running.
    if argsFile['remoteip'] == "192.168.1.1": 
        print("You MUST edit the 'args.json' file with the non-default information.")
        exit(1)

    # Creates the string to use for the remote server to upload to.
    remote = argsFile['remoteuser'] + "@" + argsFile['remoteip'] + ":" + argsFile['remotedir']

    # Runs rsync.
    rsync = subprocess.run(["rsync", "-raz", "/home/replication/local/", remote])

    # If rsync returns non-zero exit code, script exits.
    if rsync.returncode != 0:
        print("rsync upload return code non-zero, assuming failed.")
        exit(1)

remoteSSHKeyRetrieval()
rsyncUpload()

# p = subprocess.run(['ls', '-al'], capture_output=True)

