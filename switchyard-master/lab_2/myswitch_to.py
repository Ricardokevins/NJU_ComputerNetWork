'''
Ethernet learning switch in Python.

Note that this file currently has the code to implement a "hub"
in it, not a learning switch.  (I.e., it's currently a switch
that doesn't learn.)
'''
from switchyard.lib.userlib import *
import time
class info:  
    def __init__(self,create_times,ports,addresses):
        self.create_time=create_times
        self.port=ports
        self.address=addresses

def main(net):
    boardcast_addr="ff:ff:ff:ff:ff:ff"
    my_interfaces = net.interfaces() 
    mymacs = [intf.ethaddr for intf in my_interfaces]
    list_info=[]
    while True:
        try:
            timestamp,input_port,packet = net.recv_packet()
        except NoPackets:
            continue
        except Shutdown:
            return   

        index=0
        while index<len(list_info):
            temp_time=time.time()
            if temp_time-list_info[index].create_time>=10:
                del(list_info[index])
            else:
                index+=1

        log_debug ("In {} received packet {} on {}".format(net.name, packet, input_port))

        log_info ("In {} received packet {} on {}".format(net.name, packet, input_port))

        if packet[0].dst in mymacs:
            log_debug ("Packet intended for me")
        else:         
            if packet[0].dst == boardcast_addr:
                flag=0
                for i in list_info:
                    if i.address== packet[0].src:
                        flag=1
                        if i.port != input_port:
                            i.port=input_port
                            i.create_time=time.time()
                        break
                if flag==0:
                    cur_time=time.time()
                    temp=info(cur_time,input_port,packet[0].src)
                    list_info.append(temp)

                for intf in my_interfaces:
                    if input_port != intf.name:
                        log_debug ("Flooding packet {} to {}".format(packet, intf.name))
                        net.send_packet(intf.name, packet)
                        log_info ("boardcast packet from {} to {}".format(input_port, intf.name))
            else:
                flag=0
                for i in list_info:
                    if i.address== packet[0].src:
                        flag=1
                        if i.port != input_port:
                            i.port=input_port
                            i.create_time=time.time()
                        break
                if flag==0:
                    cur_time=time.time()
                    temp=info(cur_time,input_port,packet[0].src)
                    list_info.append(temp)
                
                send_flag=0
                for i in list_info:
                    if i.address==packet[0].dst:
                        net.send_packet(i.port, packet)
                        log_info ("find port {} of address {}".format(i.port,packet[0].dst))
                        send_flag=1
                        break
                
                if send_flag!=1:
                    print("didn't find port")
                    for intf in my_interfaces:
                        if input_port != intf.name:
                            log_debug ("Flooding packet {} to {}".format(packet, intf.name))   
                            net.send_packet(intf.name, packet)
                            log_info ("didnt find packet from {} to {}".format(input_port, intf.name))
                            

    net.shutdown()