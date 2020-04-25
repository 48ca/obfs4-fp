#!/usr/bin/env bash

USER=james

if [ $EUID -ne 0 ]
then
    echo "Run as root (for tcpdump) (remember to use -E if using sudo)"
    exit 127
fi

CAPDIR=${CAPDIR:auto-caps}
IF=${IF:-wlp58s0}

if ! [ -d $CAPDIR ]
then
    mkdir -p $CAPDIR
fi

echo "Writing captures in directory: $CAPDIR"


HOST=$BRIDGE
echo "Bridge: $HOST"
# HOST="195.201.102.54"
# HOST="98.243.200.229" # :1025 6ABC00A82B5A76E9B30BAED58AC7911E6BD50ADB
# HOST="212.51.128.98" # :9001 EA8FDDF7BDC90946630725AEE746AECE2D7B9714

if [ -z "$1" ]
then
    f="test"
else
    f="$CAPDIR/$1-$2"
fi

echo -e "\nWriting to $f.pcap\n"
sleep 1

# tcpdump "tcp[tcpflags] != tcp-syn and tcp[tcpflags] != tcp-ack and (dst host $HOST or src host $HOST)" -i $IF -w $f.pcap &
tcpdump "dst host $HOST or src host $HOST" -i $IF -w $f.pcap &

PID=$!

sudo -u $USER ./main.py "http://$1"

RETCODE=$?

kill -2 $PID

sleep 1
echo -e "\nDONE writing to $f.pcap\n"

if [ $RETCODE -ne 0 ]
then
    echo "FAILED $1 $2"
    mv $f.pcap $f.pcap.bad
    exit 1
fi
