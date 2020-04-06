#!/usr/bin/env bash

USER=james

if [ $EUID -ne 0 ]
then
    echo "Run as root (for tcpdump) (remember to use -E if using sudo)"
    exit 1
fi

CAPDIR=${CAPDIR:auto-caps}
IF=${IF:-wlp58s0}

if ! [ -d $CAPDIR ]
then
    mkdir -p $CAPDIR
fi

echo "Writing captures in directory: $CAPDIR"

RETRY="$1"


HOST=$BRIDGE
echo "Bridge: $HOST"
# HOST="195.201.102.54"
# HOST="98.243.200.229" # :1025 6ABC00A82B5A76E9B30BAED58AC7911E6BD50ADB
# HOST="212.51.128.98" # :9001 EA8FDDF7BDC90946630725AEE746AECE2D7B9714

caponion() {

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
        mv $f.pcap $f.pcap.BAD
        retrynum=${3:-0}
        if [ $retrynum -lt 2 ]
        then
            echo "RETRYING $1 $2 $3"
            caponion $1 $2 $((retrynum + 1))
        fi
    fi

}

captrials() {
    for i in $(seq $2 $3)
    do
        caponion $1 $i
    done
}

# captrials "facebookcorewwwi.onion" 1 8
# captrials "bbcnewsv2vjtpsuy.onion" 1 8
# captrials "3g2upl4pq6kufc4m.onion" 1 8
# captrials "rougmnvswfsmd4dq.onion" 1 8
# captrials "wlupld3ptjvsgwqw.onion" 1 8
# captrials "hdwikivgmzfa5eui.onion" 1 8

# captrials "3g2upl4pq6kufc4m.onion" 1 8 # duckduckgo
# captrials "bbcnewsv2vjtpsuy.onion" 1 8 # bbc
# captrials "facebookcorewwwi.onion" 1 8 # facebook
# captrials "rougmnvswfsmd4dq.onion" 1 8 # tor metrics
# captrials "wlupld3ptjvsgwqw.onion" 1 8 # wikileaks
# captrials "hdwikivgmzfa5eui.onion" 1 8 # hidden wiki
# captrials "hss3uro2hsxfogfq.onion" 1 8 # not evil
# captrials "msydqstlz2kzerdg.onion" 1 8 # ahmia
# captrials "onions53ehmf4q75.onion" 1 8 # oniontree
# captrials "wlchatc3pjwpli5r.onion" 1 8 # wikileaks chat (static page)
#
# chown -R $USER:users $CAPDIR

# look for retransimission
# sequence number
# aggregate packets
