from switchyard.lib.userlib import *
import time
import ipaddress
from random import randint

class Rule():
    def __init__(self,modes=None,netmodes=None,srcs=None,dsts=None,srcports=None,dstports=None,ratelimits=None,impairs=None):
        self.mode=modes
        self.netmode=netmodes
        self.src=srcs
        self.dst=dsts
        self.srcport=srcports
        self.dstport=dstports
        self.ratelimit=ratelimits
        self.impair=impairs
    def show_info(self):
        print(self.mode,self.netmode,self.src,self.srcport,self.dst,self.dstport,self.ratelimit,self.impair)

def possesse_file():
    Rule_List=[]
    with open("firewall_rules.txt") as file:
        while 1:
            line = file.readline()
            if not line:
                break    
            else:
                while line.isspace():
                    line = file.readline()
                line=line.strip('\n')
                d=line.split(" ")
                if d[0]!='#':
                    temp=Rule()            
                    temp.mode=d[0]
                    temp.netmode=d[1]
                    temp.src=d[3]
                    if "srcport" in line:
                        temp.srcport=d[5]
                        temp.dst=d[7]
                        temp.dstport=d[9]
                    else:
                        temp.dst=d[5]
                    if "ratelimit" in line:
                        for i in range(len(d)):
                            if d[i]== "ratelimit":
                                temp.ratelimit=d[i+1]
                                break
                    if "impair" in line:
                        temp.impair=True
                    else:
                        temp.impair=False
                    Rule_List.append(temp)
                    
    return Rule_List
                

def match_ip(rule,packet):
    flag=1
    if packet.has_header(IPv4):
        if rule.src !="any":
            net1=IPv4Network(rule.src,strict=False)
            if int(net1.network_address) & int(packet[IPv4].src) != int(net1.network_address):
                flag=0
        if rule.dst !="any":
            net1=IPv4Network(rule.dst,strict=False)
            if int(net1.network_address) & int(packet[IPv4].dst) != int(net1.network_address):
                flag=0
    else:
        flag=0
    return flag

def match_udp(rule,packet):
    flag=1
    if packet.has_header(IPv4):
        if rule.src !="any":
            net1=IPv4Network(rule.src,strict=False)
            if int(net1.network_address) & int(packet[IPv4].src) != int(net1.network_address):
                flag=0
        if rule.dst !="any":
            net1=IPv4Network(rule.dst,strict=False)
            if int(net1.network_address) & int(packet[IPv4].dst) != int(net1.network_address):
                flag=0 
    else:
        flag=0
    if packet.has_header(UDP):
        if rule.srcport !="any" and int(rule.srcport) != packet[UDP].src:
            flag=0
        if rule.dstport !='any' and int (rule.dstport)!=packet[UDP].dst:
            flag=0
    else:
        flag=0       
    return flag

def match_tcp(rule,packet):
    flag=1
    if packet.has_header(IPv4):
        if rule.src !="any":
            net1=IPv4Network(rule.src,strict=False)
            if int(net1.network_address) & int(packet[IPv4].src) != int(net1.network_address):
                flag=0
        if rule.dst !="any":
            net1=IPv4Network(rule.dst,strict=False)
            if int(net1.network_address) & int(packet[IPv4].dst) != int(net1.network_address):
                flag=0 
    else:
        flag=0
    if packet.has_header(TCP):
        if rule.srcport !="any" and int(rule.srcport) != packet[TCP].src:
            flag=0
        if rule.dstport !='any' and int (rule.dstport)!=packet[TCP].dst:
            flag=0
    else:
        flag=0       
    return flag

def match_icmp(rule,packet):
    flag=1
    if packet.has_header(IPv4):
        if rule.src !="any":
            net1=IPv4Network(rule.src,strict=False)
            if int(net1.network_address) & int(packet[IPv4].src) != int(net1.network_address):
                flag=0
        if rule.dst !="any":
            net1=IPv4Network(rule.dst,strict=False)
            if int(net1.network_address) & int(packet[IPv4].dst) != int(net1.network_address):
                flag=0
    else:
        flag=0
    if  not packet.has_header(ICMP):
        flag=0
    return flag

def match_rule(rule,packet):
    if rule.netmode =="ip":
        return match_ip(rule,packet)
    if rule.netmode=="udp":
        return match_udp(rule,packet)
    if rule.netmode=="tcp":
        return match_tcp(rule,packet)
    else:
        return match_icmp(rule,packet)
    


    

def main(net):
    # assumes that there are exactly 2 ports
    portnames = [ p.name for p in net.ports() ]
    portpair = dict(zip(portnames, portnames[::-1]))
    rules=possesse_file()
    index=0
    token_bucket={}
    for i in rules:
        if i.ratelimit!=None:
            token_bucket[index]=0
        index+=1
    cur_time=time.time()
    set_time=time.time()
    while True:
        pkt = None
        try:
            timestamp,input_port,pkt = net.recv_packet(timeout=0.5)
        except NoPackets:
            pass
        except Shutdown:
            break
        cur_time=time.time()
        if cur_time-set_time>0.5:
            for i in token_bucket:   
                if token_bucket[i]<int(rules[i].ratelimit)*2:
                    token_bucket[i]+=int(rules[i].ratelimit)/2        
            set_time=time.time()
        if pkt is not None:

            # This is logically where you'd include some  firewall
            # rule tests.  It currently just forwards the packet
            # out the other port, but depending on the firewall rules
            # the packet may be dropped or mutilated.
            #print(str(pkt),input_port)
            index=0
            match_flag=0
            for i in rules:
                index+=1
                if match_rule(i,pkt):
                    match_flag=1
                    break
            if match_flag: 
                print("Match rule index",index)
            else:
                print("No match")
            if match_flag:
                if rules[index-1].mode=="permit":  
                    send_flag=1
                    if rules[index-1].impair:
                        temp=randint(1,100)
                        if temp<5:
                            send_flag=0
                    if send_flag:
                        if rules[index-1].ratelimit!=None:
                            use_size=len(pkt)-len(pkt.get_header(Ethernet))
                            if use_size<=token_bucket[index-1]:
                                token_bucket[index-1]-=use_size
                                net.send_packet(portpair[input_port], pkt)
                        else:
                            net.send_packet(portpair[input_port], pkt)
            else:
                net.send_packet(portpair[input_port], pkt)


            
    net.shutdown()
  

# testcase 
# external ./www/start_webserver.sh 8000
# internal wget http://192.168.0.2:8000/bigfile -O /dev/null