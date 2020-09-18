#!/usr/bin/env python3
'''
Ethernet hub in Switchyard.
'''
from switchyard.lib.userlib import *


def main(net):
    my_interfaces = net.interfaces()
    mymacs = [intf.ethaddr for intf in my_interfaces]
    in_num=0
    out_num=0
    while True:
        try:
            timestamp, dev, packet = net.recv_packet()
            in_num+=1
        except NoPackets:
            continue
        except Shutdown:
            return
        log_debug("In {} received packet {} on {}".format(
            net.name, packet, dev))
        eth = packet.get_header(Ethernet)
        if eth is None:
            log_info("Received a non-Ethernet packet?!")
            continue

        if eth.dst in mymacs:
            log_info("Received a packet intended for me")
        else:
            #print("before loop")
            for intf in my_interfaces:
                #print("testcase1:",intf.name)
                #print("testcase2:",dev)
                if dev != intf.name:
                    log_info("Flooding packet {} to {}".format(
                        packet, intf.name))
                    net.send_packet(intf, packet)
                    out_num+=1
                    log_info("in:{}  out:{}".format(in_num, out_num))
    net.shutdown()
