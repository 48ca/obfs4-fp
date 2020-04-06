#!/bin/bash

# from https://witestlab.poly.edu/blog/de-anonymizing-tor-traffic-with-website-fingerprinting/

if [ $UID -ne 0 ]
then
    echo "Run as root please"
    exit 1
fi

set -x

IF=${IF:-wlp58s0}

ethtool -K $IF gro off
ethtool -K $IF gso off
ethtool -K $IF tso off
