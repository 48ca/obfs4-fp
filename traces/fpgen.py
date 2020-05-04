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
    onions = set(f.read().split("\n")[:-1])

for p in ("BRIDGE", "IF", "SRCMAC", "CAPDIR", "LOGFILE"):
    print("{}:{}{}".format(p, " " * (10-len(p)), os.getenv(p)))

try:
    i = input("Are the env vars correct? [Y/n]: ")
except EOFError:
    print()
    sys.exit(1)
if len(i) > 0 and i[0].lower() == "n":
    sys.exit(1)

print("Fetching {} webpages".format(len(onions)))

paused = False
stopped = False
done = 0
round = 0

MAX_ROUNDS = 40
if len(sys.argv) > 1:
    MAX_ROUNDS = int(sys.argv[1])
    print("Performing {} rounds".format(MAX_ROUNDS))

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
    failed_gen1  = set() # initial failed set
    failed_gen2  = set() # if failed in two rounds
    failed_final = set() # if failed in three rounds
    for r in range(MAX_ROUNDS):
        done = 0
        round = r
        failed = set()
        if len(failed_final) > 0:
            print("Not fetching {} onions".format(len(failed_final)))
        for u in urls - failed_final:
            while paused and not stopped:
                time.sleep(1)
            if stopped:
                break
            if dump(u, r):
                done += 1
            else:
                failed.add(u)
        if len(failed) > 0:
            print("Checking failed onions...")
        real_failed = set()
        for u in failed:
            while paused and not stopped:
                time.sleep(1)
            if stopped:
                break
            if not dump(u, r):
                print("Could not fetch {} after two attempts".format(u))
                real_failed.add(u)
            done += 1

        failed_final |= failed_gen2 & failed_gen1 & real_failed
        failed_gen2 = failed_gen1
        failed_gen1 = real_failed

        if stopped:
            return
        print("Iteration done")
    print("All rounds done")
    print("Failed onions:")
    print(failed_final)


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
