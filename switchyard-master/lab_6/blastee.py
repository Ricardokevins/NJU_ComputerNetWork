#!/usr/bin/env python3

from switchyard.lib.address import *
from switchyard.lib.packet import *
from switchyard.lib.userlib import *
from threading import *
import time

def switchy_main(net):
    my_interfaces = net.interfaces()
    mymacs = [intf.ethaddr for intf in my_interfaces]
    file = open("blastee_params.txt")
    line = file.readline()
    line=line.strip('\n')
    d=line.split(" ")
    ip=d[1]
    num=d[3]
    while True:
        gotpkt = True
        try:
            timestamp,dev,pkt = net.recv_packet()
            log_debug("Device is {}".format(dev))
        except NoPackets:
            log_debug("No packets available in recv_packet")
            gotpkt = False
        except Shutdown:
            log_debug("Got shutdown signal")
            break

        if gotpkt:
            #log_info("I got a packet from {}".format(dev))
            #log_info("Pkt: {}".format(pkt))
            #seq=int.from_bytes(pkt[3][0:4], byteorder='big', signed=False)
            #payload=int.from_bytes(pkt[3][6:14], byteorder='big', signed=False)
            #print(seq)
            #print(payload)
            seq2=pkt[3].to_bytes()[0:4]
            payload2=pkt[3].to_bytes()[6:14]
            #print(seq2)
            #print(payload2)
            seq=int.from_bytes(seq2, byteorder='big', signed=False)
            payload=int.from_bytes(payload2, byteorder='big', signed=False)
            print(seq)
            #print(payload)

            pkt = Ethernet() + IPv4() + UDP()
            pkt[1].protocol = IPProtocol.UDP
            pkt += seq2
            pkt += payload2
            pkt[Ethernet].src=EthAddr('20:00:00:00:00:01')
            pkt[IPv4].src=IPv4Address('192.168.200.1')
            pkt[Ethernet].dst=EthAddr('10:00:00:00:00:01')
            pkt[IPv4].dst=IPv4Address(ip)
            net.send_packet(my_interfaces[0],pkt)


    net.shutdown()
