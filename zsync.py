import subprocess
import json
from matterhook import Webhook # https://github.com/numberly/matterhook

# Gets all the json from the args.json file.
argsFile = json.load(open('args.json'))

# Mattermost setup
# Uses 'args.json' to allow Mattermost notifications.
mm = Webhook(argsFile['mmwebhook'].split('hooks')[0][:-1], argsFile['mmwebhook'].split('hooks')[-1][1:])
dirs = [[] for i in range(len(argsFile['dirstonotifyon']))]
mmattachments = []
mmmessage = {}

def mattermostNotification(goodOrBad, message=""):
    if argsFile['mmnotifications'] == "true":
        if goodOrBad == "good":
            if not any(dirs):
                mmmessage['color'] = '#0ffc03'
                mmmessage['text'] = "No updates made."
                mmattachments.append(mmmessage)
                mm.send(attachments=mmattachments)
            else:
                # Created a separate markdown message for each root level dir to by notified on.
                for idx, i in enumerate(range(len(argsFile['dirstonotifyon']))):
                    mmmessage['color'] = '#0ffc03'
                    mmmarkdown = '### ' + argsFile['dirstonotifyon'][idx] + "\n"
                    for y in dirs[idx]:
                        mmmarkdown += y + "\n"

                    mmmessage['text'] = mmmarkdown
                    mmattachments.append(mmmessage)
                    mm.send(attachments=mmattachments)
                    mmattachments.clear()
        elif goodOrBad == "bad":
            mmmessage['color'] = "#ff0000"
            mmmessage['text'] = message
            mmattachments.append(mmmessage)
            mm.send(attachments=mmattachments)
        else:
            print("This shouldn't be happening :(")
            exit(1)

def remoteSSHKeyRetrieval():
    # Runs a bash script to get the remote key and save it go /home/zsync/.ssh/known_hosts.
    subprocess.run(["/bin/bash", "retrieve-key.sh"], capture_output=True)

def rsyncUpload():
    # Checks if user edited the args.json before running.
    if argsFile['remoteip'] == "192.168.1.1": 
        print("You MUST edit the 'args.json' file with the non-default information.")
        exit(1)

    # Creates the string to use for the remote server to upload to.
    remote = argsFile['remoteuser'] + "@" + argsFile['remoteip'] + ":" + argsFile['remotedir']

    # Runs rsync.
    rsync = subprocess.run(["rsync", "-razi", "--ignore-existing", "/home/zsync/local/", remote], capture_output=True)

    # If rsync returns non-zero exit code, script exits.
    if rsync.returncode != 0:
        print("rsync upload return code non-zero, assuming failed.")
        print("rsync exit code: " + str(rsync.returncode))
        print(rsync.stdout)
        mattermostNotification("bad", "rsync upload return code non-zero, assuming failed.\nrsync return code: " + str(rsync.returncode))
        exit(1)

    rOutput = rsync.stdout.decode('utf-8')

    if argsFile['mmnotifications'] == "true":
        # Parses out the new movies & tv-shows.
        for idx, directory in enumerate(argsFile['dirstonotifyon']): # For loop with tracked index.
            for n in rOutput.split("\n"): # Splits out into new lines.
                if n.split("++++ ")[-1].split("/", 1)[0] == directory: # Splits +++ between the real info.
                    if n.split("++++ ")[-1].split("/", 1)[-1] != '': # Makes sure info isn't ''.
                        dirs[idx].append(n.split("++++ ")[-1].split("/", 1)[-1]) # Appends to appropriate list.

remoteSSHKeyRetrieval()
rsyncUpload()
mattermostNotification("good")