#!/usr/bin/env python3

'''
Basic IPv4 router (static routing) in Python.
'''

import sys
import os
import time
from switchyard.lib.userlib import *



class Router(object):
    def __init__(self, net):
        self.net = net
        # other initialization stuff here
        self.interfaces = net.interfaces() 
        self.ip_list=[intf.ipaddr for intf in self.interfaces]
        self.mac_list=[intf.ethaddr for intf in self.interfaces]
        self.arp_table={}
        
    def router_main(self):    
        '''
        Main method for router; we stay in a loop in this method, receiving
        packets until the end of time.
        '''
        while True:
            gotpkt = True
            try:
                timestamp,dev,pkt = self.net.recv_packet(timeout=1.0)
            except NoPackets:
                log_debug("No packets available in recv_packet")
                gotpkt = False
            except Shutdown:
                log_debug("Got shutdown signal")
                break
            
            if gotpkt:
                log_debug("Got a packet: {}".format(str(pkt)))
                log_info("Got a packet: {}".format(str(pkt)))
                arp = pkt.get_header(Arp)
                if arp is None:
                    log_info("Not arp Packet")
                else:
                    log_info("operation kind {}".format(str(arp.operation)))
                    self.arp_table[arp.senderprotoaddr]=arp.senderhwaddr
                    if arp.operation == 1:
                        log_info("recive arp requests")
                        index=-1
                        for i in range(len(self.ip_list)):
                            if self.ip_list[i]==arp.targetprotoaddr:
                                index=i
                                break
                        if index != -1:
                            log_info("match the packet")
                            answer=create_ip_arp_reply(self.mac_list[index], arp.senderhwaddr, self.ip_list[index],arp.senderprotoaddr)
                            self.net.send_packet(dev, answer)
                            log_info("send answer: {}".format(str(answer)))
                        else:
                            log_info("no match")
                    else:
                        if arp.operation == 2:
                            log_info("recive arp reply")
                            self.arp_table[arp.targetprotoaddr]=arp.targethwaddr
                        else:
                            log_info("recive unk arp")
                log_info("Table Shown as follows")
                for (k,v) in  self.arp_table.items(): 
                    print ("%s     " % k,v )
                
                        
                    





def main(net):
    '''
    Main entry point for router.  Just create Router
    object and get it going.
    '''
    r = Router(net)
    r.router_main()
    net.shutdown()
