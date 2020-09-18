#!/usr/bin/env python3

from switchyard.lib.address import *
from switchyard.lib.packet import *
from switchyard.lib.userlib import *
from threading import *
from random import randint
import time

def switchy_main(net):

    my_intf = net.interfaces()
    mymacs = [intf.ethaddr for intf in my_intf]
    myips = [intf.ipaddr for intf in my_intf]

    file = open("middlebox_params.txt")
    line = file.readline()
    line=line.strip('\n')
    d=line.split(" ")
    c=float(d[1])
    c*=100
    print(c)
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
            log_debug("I got a packet {}".format(pkt))

        if dev == "middlebox-eth0":
            log_debug("Received from blaster")
            '''
            Received data packet
            Should I drop it?
            If not, modify headers & send to blastee
            '''
            temp=randint(1,100)
            if temp <= c:
                print("Packet drop")
            else:
                pkt[Ethernet].dst=EthAddr('20:00:00:00:00:01')
                seq2=pkt[3].to_bytes()[0:4]
                seq3=int.from_bytes(seq2, byteorder='big', signed=False)
                net.send_packet("middlebox-eth1", pkt)
                print("send pac"," ",seq3)
        elif dev == "middlebox-eth1":
            log_debug("Received from blastee")
            '''
            Received ACK
            Modify headers & send to blaster. Not dropping ACK packets!
            net.send_packet("middlebox-eth0", pkt)
            '''
            pkt[Ethernet].dst=EthAddr('10:00:00:00:00:01')
            net.send_packet("middlebox-eth0", pkt)
            seq2=pkt[3].to_bytes()[0:4]
            seq3=int.from_bytes(seq2, byteorder='big', signed=False)
            print("send ACK ",seq3)
        else:
            log_debug("Oops :))")

    net.shutdown()
