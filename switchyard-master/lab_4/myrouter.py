#!/usr/bin/env python3

'''
Basic IPv4 router (static routing) in Python.
'''

import sys
import os
import time
from switchyard.lib.userlib import *
import ipaddress
import queue



class Node():
    def __init__(self,p,m,n,i):
        self.prefix=p
        self.mask=m
        self.nexthop=n
        self.name=i
#swyard -t routertests2.srpy myrouter.py

class Pac():
    def __init__(self,pac,thing):
        self.pac=pac 
        self.ci=0
        self.time=0
        self.th=thing

class Router(object):
    def __init__(self, net):
        self.net = net
        # other initialization stuff here
        self.interfaces = net.interfaces() 
        self.ip_list=[intf.ipaddr for intf in self.interfaces]
        self.mac_list=[intf.ethaddr for intf in self.interfaces]
        self.arp_table={}
        self.forward_table=[]
        for i in self.interfaces:      
            #print(i.name)
            #print(i.netmask)
            #print(i.ipaddr)
            #print("a:")
            
            #prefix=ipaddress.IPv4Address(str(i.ipaddr)+"/"+str(i.netmask))

            prefix=ipaddress.ip_network(str(i.ipaddr)+"/"+str(i.netmask), strict=False)
            prefix=str(prefix)
            if '/' in  prefix:
                prefix=prefix.split("/")
                prefix=prefix[0]
            #print(prefix)
            prefix=IPv4Address(prefix)
            #print(i.ipaddr)
            #print("end")
            #print(type(prefix))
            #print(type(i.netmask))
            a=Node(prefix,i.netmask,None,i.name)     
            self.forward_table.append(a)
        
        file = open("forwarding_table.txt")
        while 1:
            line = file.readline()
            if not line:
                break
            else:
                line=line.strip('\n')
                d=line.split(" ")
                a=Node(IPv4Address(d[0]),IPv4Address(d[1]),IPv4Address(d[2]),d[3])
                self.forward_table.append(a)
        for a in self.forward_table:
            print(a.prefix," ",a.mask," ",a.nexthop," ",a.name)

    def router_main(self):    
        '''
        Main method for router; we stay in a loop in this method, receiving
        packets until the end of time.
        '''
        q = []
        while True:
            if len(q)!=0: 
                for i in self.interfaces:
                    if i.name==q[0].th.name:
                        port=i
                if q[0].th.nexthop is None:
                    targetip=q[0].pac[IPv4].dst
                else:
                    targetip=q[0].th.nexthop
                find_flag2=0
                for (k,v) in  self.arp_table.items(): 
                    if targetip == k:
                        q[0].pac[Ethernet].dst=v
                        q[0].pac[Ethernet].src=port.ethaddr   
                        print("send pac (find) ",port)                     
                        self.net.send_packet(port,q[0].pac)
                        find_flag2=1
                        del(q[0])
                        break

                if find_flag2 ==0:
                    if q[0].ci >= 5:
                        del(q[0])
                    else:
                        cur=time.time()
                        if (q[0].ci==0) or (cur-q[0].time)>1:
                            ether = Ethernet()               
                            ether.src = port.ethaddr
                            ether.dst = 'ff:ff:ff:ff:ff:ff'
                            ether.ethertype = EtherType.ARP            
                            arp = Arp(operation=ArpOperation.Request,senderhwaddr=port.ethaddr,senderprotoaddr=port.ipaddr,targethwaddr='ff:ff:ff:ff:ff:ff',targetprotoaddr=targetip)
                            arppacket = ether + arp    
                            print("send requests",port) 
                            self.net.send_packet(port, arppacket)
                            q[0].ci+=1 
                            q[0].time=time.time()
                            print(q[0].time) 
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
                if pkt.has_header(IPv4):
                    head=(pkt[IPv4])
                    if head is None:
                        print("error")
                    head.ttl-=1
                    print("ipv4",head)
                    pos=-1
                    prefixlen=-1
                    index=0
                    for i in self.forward_table:
                        if ((int(head.dst)&int(i.mask))==int(i.prefix)):
                            netaddr = IPv4Network(str(i.prefix)+"/"+str(i.mask))
                            if netaddr.prefixlen > prefixlen:
                                prefixlen=netaddr.prefixlen
                                pos=index
                            #print("Match")  
                        index+=1
                    print("add packet to queue")     
                    if pos == -1:
                        print("No Match Some Error occur!!!!!!!!!!!!!!!!!")       
                    else:
                        q.append(Pac(pkt,self.forward_table[pos]))
                    """
                    find_flag = 0    
                    for (k,v) in  self.arp_table.items(): 
                        if self.forward_table[pos].nexthop !=None:
                            if self.forward_table[pos].nexthop==k:
                                pkt[Ethernet].dst=v
                                
                                print("hit1")
                                self.net.send_packet(self.forward_table[pos].name, pkt)
                                find_flag = 1
                        else:
                            if head.dst == k:
                                pkt[Ethernet].dst=v
                                print("hit2")
                                self.net.send_packet(self.forward_table[pos].name, pkt)
                                find_flag=1
                    if find_flag !=1 :
                    """
                        
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