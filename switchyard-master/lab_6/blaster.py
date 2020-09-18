#!/usr/bin/env python3

from switchyard.lib.address import *
from switchyard.lib.packet import *
from switchyard.lib.userlib import *
from random import randint
import time

class Node():
    def __init__(self,pacs,seqs):
        self.pac=pacs
        self.seq=seqs
        self.flag=0


def switchy_main(net):
    my_intf = net.interfaces()
    mymacs = [intf.ethaddr for intf in my_intf]
    myips = [intf.ipaddr for intf in my_intf]
    file = open("blaster_params.txt")
    line = file.readline()
    line=line.strip('\n')
    d=line.split(" ")
    print(d)
    ip=d[1]
    num=d[3]
    length=d[5]
    window=d[7]
    timeout=d[9]
    timeout=float(timeout)/1000
    timeout=1
    print(timeout)
    rev_time=d[11]
    rev_time=float(rev_time)/1000
    q=[]
    seq=1
    LHS=1
    RHS=1
    starttime=time.time()
    timer=time.time()
    cur=time.time()

    retrainsport=0
    timeout_times=0
    while True:
        print(LHS," ",RHS," ",seq)
        gotpkt = True
        try:
            #Timeout value will be parameterized!
            timestamp,dev,pkt = net.recv_packet(timeout=rev_time)
        except NoPackets:
            log_debug("No packets available in recv_packet")
            gotpkt = False
        except Shutdown:
            log_debug("Got shutdown signal")
            break

        if gotpkt:
            seq2=pkt[3].to_bytes()[0:4]
            seq3=int.from_bytes(seq2, byteorder='big', signed=False)
            for i in q:
                if i.seq==seq3:
                    print(seq3,"Has Acked")
                    i.flag=1
            while len(q)>0:
                if q[0].flag==1:
                    LHS = q[0].seq+1
                    del(q[0])   
                    cur=time.time()        
                else:
                    break
        else:
            log_debug("Didn't receive anything")

            '''
            Creating the headers for the packet
            '''
            if seq>int(num) and len(q)==0:
                endtime=time.time()
                TotalTime=endtime-starttime
                print("Total time",TotalTime)
                print("Number of reTX: ",retrainsport)
                print("Number of coarse TOs: ",timeout_times)
                print("Throughput (Bps): ",(retrainsport+int(num))*int(length)/TotalTime)
                print("Goodput (Bps): ",int(num)*int(length)/TotalTime)
                exit()
            timer=time.time()
            print("timer",timer," ",cur)
            if timer-cur>timeout:           
                for i in q:
                    if i.flag==0:
                        print("Timeout resend ",i.seq)
                        net.send_packet(my_intf[0],i.pac)
                        timeout_times+=1
                        retrainsport+=1
                        break
            else:
                if RHS-LHS+1 < int(window) and seq<=int(num):
                    print("able to send  ",seq)
                    pkt = Ethernet() + IPv4() + UDP()
                    pkt[1].protocol = IPProtocol.UDP
                    pkt += seq.to_bytes(4,byteorder='big', signed=False)
                    pkt += int(length).to_bytes(2,byteorder='big', signed=False)
                    payload = b'These are some application data bytes'
                    payload=payload[0:int(length)-1]
                    pkt+=payload
                    pkt[Ethernet].dst=EthAddr('20:00:00:00:00:01')
                    pkt[IPv4].dst=IPv4Address(ip)
                    pkt[Ethernet].src=EthAddr('10:00:00:00:00:01')
                    pkt[IPv4].src=IPv4Address('192.168.100.1')
                    RHS=seq
                    temp=Node(pkt,seq)
                    q.append(temp)
                    seq+=1
                    net.send_packet(my_intf[0],pkt)
                   
                    
            

            '''
            Do other things here and send packet
            '''

    net.shutdown()
