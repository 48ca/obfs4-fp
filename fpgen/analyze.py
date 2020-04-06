#!/usr/bin/env python3

from pcapfile import savefile
import matplotlib.pyplot as plt
from pcapfile.protocols.linklayer import ethernet
from pcapfile.protocols.network import ip
from pcapfile.protocols.transport import tcp
import binascii

from sys import argv, stderr, stdout, exit
from os import getenv

if len(argv) == 1:
    print('no file specified. using test.pcap')
    file = 'test.pcap'
else:
    file = argv[1]

noplot = False
if len(argv) > 2:
    noplot = (argv[2] == "--noplot")

testcap = open(file, 'rb')
capfile = savefile.load_savefile(testcap, verbose=True)

print(capfile)

bridge = getenv("BRIDGE", "195.201.102.54").encode('ascii')

x_in = []
y_in = []
x_out = []
y_out = []
outgoing_packets = 0
incoming_packets = 0
outgoing_total_bytes = 0
incoming_total_bytes = 0
final_timestamp = 0
seqnums = set()
packet_lengths = [0 for i in range(1500)]
packet_directions = []

if len(capfile.packets) == 0:
    print("No packets")
    exit(1)

for p in capfile.packets:
    eth_frame = ethernet.Ethernet(p.raw())
    tcp_packet = tcp.TCP(binascii.unhexlify(eth_frame.payload))
    if tcp_packet.seqnum in seqnums:
        continue
    seqnums.add(tcp_packet.seqnum)
    ip_packet = ip.IP(binascii.unhexlify(eth_frame.payload))
    final_timestamp = p.timestamp_ms
    if (ip_packet.len < 1500):
        packet_lengths[ip_packet.len] = 1
    if (ip_packet.dst == bridge):
        packet_directions.append(1)
        outgoing_packets += 1
        x_out.append(p.timestamp_ms)
        y_out.append(ip_packet.len)
        outgoing_total_bytes += ip_packet.len
    else:
        packet_directions.append(-1)
        incoming_packets += 1
        x_in.append(p.timestamp_ms)
        y_in.append(ip_packet.len)
        incoming_total_bytes += ip_packet.len

packet_directions = packet_directions[:5000]
print(len(packet_directions))

total_packets = outgoing_packets + incoming_packets
retransmissions = len(capfile.packets) - len(seqnums)

# def auxprint(*args):
#     stderr.write("{}\n".format("{}" * len(args)).format(*args))

print("::> name: ", file)
print(":: outgoing packets: ", outgoing_packets)
print(":: incoming packets: ", incoming_packets)
print(":: total packets: ", total_packets)
print(":: outp/t packets: ", outgoing_packets / total_packets)
print(":: incp/t packets: ", incoming_packets / total_packets)
print(":: inc total bytes: ", incoming_total_bytes)
print(":: out total bytes: ", outgoing_total_bytes)
print(":: retransmissions: ", retransmissions)
print(":: final timestamp: ", final_timestamp)

name = file[file.rindex('/'):]
name = name[1:name.find('.')]

dir = 1
idx = 0
directions = [0]
for i in range(len(packet_directions)):
    if packet_directions[i] == dir:
        directions[idx] += 1
    else:
        directions.append(1)
        idx += 1
        dir = -1 * dir

print(directions)

if not noplot:
    ax_in = plt.scatter(x_in, y_in, label='in')
    ax_out = plt.scatter(x_out, y_out, label='out')
    plt.legend()
    plt.show()
else:
    if (incoming_packets != 0 and outgoing_packets != 0):
        stdout.write("!csv: {},{},{},{},{},{},{},{},{},{}".format(name, outgoing_packets,
            incoming_packets, total_packets, outgoing_packets/total_packets,
            incoming_packets/total_packets,
            incoming_total_bytes, outgoing_total_bytes,
            retransmissions, final_timestamp))
        for i in packet_lengths:
            stdout.write(",{}".format(i))
        for i in range(len(packet_directions)):
            stdout.write(",{}".format(packet_directions[i]))
        for i in range(5000 - len(packet_directions)):
            stdout.write(",{}".format(0))
