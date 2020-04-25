#export IF=wlp58s0
export IF=enp57s0u1u4
#export SRCMAC="2c:4d:54:e9:4f:e8"
export SRCMAC="$(cat /sys/class/net/$IF/address)"
export CAPDIR=dumps/IAT3-EXTRAPACKETS-Mar30
export LOGFILE=logs/dynaflow.log

# export BRIDGE=107.161.172.101
# export BRIDGE=46.140.72.219
export BRIDGE=64.227.28.1

source ../venv/bin/activate
