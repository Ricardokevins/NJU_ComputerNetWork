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

def mk_icmperr(hwsrc, hwdst, ipsrc, ipdst, xtype, xcode=0, origpkt=None, ttl=64):
    ether = Ethernet()
    ether.src = EthAddr(hwsrc)
    ether.dst = EthAddr(hwdst)
    ether.ethertype = EtherType.IP
    ippkt = IPv4()
    ippkt.src = IPAddr(ipsrc)
    ippkt.dst = IPAddr(ipdst)
    ippkt.protocol = IPProtocol.ICMP
    ippkt.ttl = ttl
    ippkt.ipid = 0
    icmppkt = ICMP()
    icmppkt.icmptype = xtype
    icmppkt.icmpcode = xcode
    if origpkt is not None:
        xpkt = deepcopy(origpkt)
        i = xpkt.get_header_index(Ethernet)
        if i >= 0:
            del xpkt[i]
        icmppkt.icmpdata.data = xpkt.to_bytes()[:28]
        icmppkt.icmpdata.origdgramlen = len(xpkt)

    return ether + ippkt + icmppkt 

def deal_with_ping(packet,dstip):
    ether = Ethernet()
    ether.ethertype = EtherType.IP
    ippkt = IPv4()
    ippkt.src = IPAddr(dstip)
    ippkt.dst = IPAddr(packet[IPv4].src)
    ippkt.protocol = IPProtocol.ICMP
    ippkt.ttl = 64
    ippkt.ipid = 0

    icmppkt = ICMP()
    icmppkt.icmptype = ICMPType.EchoReply
    icmppkt.icmpcode = ICMPCodeEchoReply.EchoReply

    icmppkt.icmpdata.sequence = packet[ICMP].icmpdata.sequence
    icmppkt.icmpdata.data = packet[ICMP].icmpdata.data

    return ether + ippkt + icmppkt 

class Node():
    def __init__(self,p,m,n,i):
        self.prefix=p
        self.mask=m
        self.nexthop=n
        self.name=i
#swyard -t routertests2.srpy myrouter.py

class Pac():
    def __init__(self,pac,thing,i=None):
        self.pac=pac 
        self.ci=0
        self.time=0
        self.th=thing
        self.icmp_info=i

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
                        print("common",targetip)
                        q[0].pac[Ethernet].dst=v
                        q[0].pac[Ethernet].src=port.ethaddr   
                        print("send pac (find) ",q[0].pac," through ",port)                     
                        self.net.send_packet(port,q[0].pac)
                        find_flag2=1
                        del(q[0])
                        break

                if find_flag2 ==0:
                    if q[0].ci >= 5:              
                        print("Time out And fail to send arp request Final Give up")
                        for i in self.interfaces:
                            if i.name==q[0].icmp_info:
                                receive_port4=i
                                break
                        
                        pkt=mk_icmperr(q[0].pac[Ethernet].dst,q[0].pac[Ethernet].src,receive_port4.ipaddr,q[0].pac[IPv4].src, ICMPType.DestinationUnreachable, xcode=1, origpkt=pkt, ttl=64)
                        head=(pkt[IPv4])
                        pos=-1
                        prefixlen=-1
                        index=0
                        for i in self.forward_table:
                            if ((int(head.dst)&int(i.mask))==int(i.prefix)):
                                netaddr = IPv4Network(str(i.prefix)+"/"+str(i.mask))
                                if netaddr.prefixlen > prefixlen:
                                    prefixlen=netaddr.prefixlen
                                    pos=index
                            index+=1
                        del(q[0])
                        print("send arp fail fix and reput in queue")              
                        immediate=Pac(pkt,self.forward_table[pos],receive_port4.name)
                        print(immediate.th.name)
                        for i in self.interfaces:
                            if i.name==immediate.th.name:
                                port=i
                        if immediate.th.nexthop is None:
                            targetip=immediate.pac[IPv4].dst
                        else:
                            targetip=immediate.th.nexthop
                        print(targetip)
                        find_flag3=0
                        for (k,v) in  self.arp_table.items(): 
                            print(k)
                            if targetip == k:
                                immediate.pac[Ethernet].dst=v
                                immediate.pac[Ethernet].src=port.ethaddr   
                                find_flag3=1
                                print("send pac (find) ",immediate.pac," through ",port)                     
                                self.net.send_packet(port,immediate.pac)
                                break
                        if find_flag3==0:
                            ether = Ethernet()               
                            ether.src = port.ethaddr
                            ether.dst = 'ff:ff:ff:ff:ff:ff'
                            ether.ethertype = EtherType.ARP            
                            arp = Arp(operation=ArpOperation.Request,senderhwaddr=port.ethaddr,senderprotoaddr=port.ipaddr,targethwaddr='ff:ff:ff:ff:ff:ff',targetprotoaddr=targetip)
                            arppacket = ether + arp    
                            print("send requests",port) 
                            self.net.send_packet(port, arppacket)
                            q.append(immediate)
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
                log_info("Got a packet: {}".format(str(pkt)))
                if pkt.has_header(IPv4):
                    head=(pkt[IPv4])
                    if head is None:
                        print("error")
                    icmp_flag=1
                    if pkt[IPv4].dst in self.ip_list:
                        print("Match router ip")
                        icmp_flag=0
                        if pkt.has_header(ICMP) :                          
                            if  pkt[ICMP].icmptype == ICMPType.EchoRequest:
                                print("ICMP ping request Packet")
                                icmp_flag=1
                                for i in self.ip_list:
                                    if i==head.dst:
                                        pkt=deal_with_ping(pkt,i)
                                        print(pkt)
                                        head=(pkt[IPv4])
                                        break
                    if icmp_flag==0:
                        print("Not ICMP request pac Hit !")
                        for i in self.interfaces:
                            if i.name==dev:
                                receive_port=i
                                break
                        print("send port",dev)
                        pkt=mk_icmperr(pkt[Ethernet].dst, pkt[Ethernet].src,receive_port.ipaddr,pkt[IPv4].src, ICMPType.DestinationUnreachable, xcode=3, origpkt=pkt, ttl=64)
                        head=(pkt[IPv4])

                    head.ttl-=1
                    if head.ttl <= 0:
                        for i in self.interfaces:
                            if i.name==dev:
                                receive_port2=i
                                break
                        pkt=mk_icmperr(pkt[Ethernet].dst, pkt[Ethernet].src,receive_port2.ipaddr,pkt[IPv4].src, 11, xcode=0, origpkt=pkt, ttl=64)
                        head=(pkt[IPv4])
                        print("TimeExceed",pkt)
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
                        index+=1             
                    if pos == -1:
                        print("No Match Some Error occur!!!!!!!!!!!!!!!!!")
                        for i in self.interfaces:
                            if i.name==dev:
                                receive_port3=i
                                break
                        pkt=mk_icmperr(pkt[Ethernet].dst, pkt[Ethernet].src,receive_port3.ipaddr,pkt[IPv4].src, 3, xcode=0, origpkt=pkt, ttl=64)
                        head=(pkt[IPv4])
                        pos=-1
                        prefixlen=-1
                        index=0
                        for i in self.forward_table:
                            if ((int(head.dst)&int(i.mask))==int(i.prefix)):
                                netaddr = IPv4Network(str(i.prefix)+"/"+str(i.mask))
                                if netaddr.prefixlen > prefixlen:
                                    prefixlen=netaddr.prefixlen
                                    pos=index
                            index+=1
                        print("refix and add packet to queue")    
                        q.append(Pac(pkt,self.forward_table[pos],dev))           
                    else:
                        print("add packet to queue")    
                        q.append(Pac(pkt,self.forward_table[pos],dev))
   
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