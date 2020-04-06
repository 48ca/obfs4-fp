#!/usr/bin/env python3

import IPython
import os
import sys
import threading
import time
import datetime
import subprocess

if os.getuid() != 0:
    print("Please run as root for tcpdump. (If using sudo, use sudo -E)")
    sys.exit(1)

with open("crawl/good-onions-med.txt", "r") as f:
    onions = f.read().split("\n")[:-1]

for p in ("BRIDGE", "IF", "SRCMAC", "CAPDIR", "LOGFILE"):
    print("{}:{}{}".format(p, " " * (10-len(p)), os.getenv(p)))

try:
    i = input("Are the env vars correct? [Y/n]: ")
except EOFError:
    print()
    sys.exit(1)
if len(i) > 1 and i[0].lower() == "n":
    sys.exit(1)

print("Fetching {} webpages".format(len(onions)))

paused = False
stopped = False
done = 0
round = 0

MAX_ROUNDS = 15

with open(os.getenv("LOGFILE"), "w") as f:
    f.write("Start trace dump at {}".format(datetime.datetime.now()))

def dump(url, trial):
    # Success -> True
    print(url)
    with open(os.getenv("LOGFILE"), "a") as f:
        e = subprocess.call(["bash", "dump-minimal.sh", url, "{}".format(trial)], stderr=f, stdout=f)
        if e == 127:
            print("Not running as root?")
            sys.exit(127)
        if e == 1:
            return False
    return True

failed = []
def fetch():
    global done, round, failed
    urls = onions.copy()
    for r in range(MAX_ROUNDS):
        done = 0
        round = r
        failed = []
        for u in urls:
            while paused and not stopped:
                time.sleep(1)
            if stopped:
                break
            if dump(u, r):
                done += 1
            else:
                failed.append(u)
        for u in failed:
            while paused and not stopped:
                time.sleep(1)
            if stopped:
                break
            if dump(u, r):
                done += 1
            else:
                print("Could not fetch {} after two attempts".format(u))

        if stopped:
            return


t = threading.Thread(target=fetch)
t.start()

### Utilities
def progress():
    print("fpgen: In current round: {}/{}".format(done, len(onions)))
    print("fpgen: Current round: {}/{}".format(round, MAX_ROUNDS))

def pause():
    global paused
    paused = True
    print("fpgen: Paused")

def unpause():
    global paused
    paused = False
    print("fpgen: Unpaused")

def stop():
    global stopped
    stopped = True
    print("fpgen: Stopping")
    t.join()
    print("fpgen: Stopped -- cannot restart")


IPython.embed()

sys.exit(0)
