'''
Ethernet learning switch in Python.

Note that this file currently has the code to implement a "hub"
in it, not a learning switch.  (I.e., it's currently a switch
that doesn't learn.)
'''
from switchyard.lib.userlib import *

class info:   
    def __init__(self,ports,addresses):
        self.port=ports
        self.address=addresses


def main(net):
    boardcast_addr="ff:ff:ff:ff:ff:ff"
    my_interfaces = net.interfaces() 
    mymacs = [intf.ethaddr for intf in my_interfaces]

    max_len=5
    list_info=[]

    while True:
        try:
            timestamp,input_port,packet = net.recv_packet()
        except NoPackets:
            continue
        except Shutdown:
            return   

        print("test info start")
        for i in list_info:
            print("add",i.address)
            print("por",i.port)
        print("test info end")

        log_debug ("In {} received packet {} on {}".format(net.name, packet, input_port))

        log_info ("In {} received packet {} on {}".format(net.name, packet, input_port))

        if packet[0].dst in mymacs:
            log_debug ("Packet intended for me")
        else:         
            if packet[0].dst == boardcast_addr:
                flag=0
                for i in range(len(list_info)):
                    if list_info[i].address== packet[0].src:
                        flag=1
                        if list_info[i].port != input_port:
                            list_info[i].port = input_port
                        break
                if flag==0:
                    if len(list_info) >=max_len:
                        for i in range(1,len(list_info)):
                            list_info[i-1]=list_info[i]
                        temp=info(input_port,packet[0].src)
                        list_info[len(list_info)-1]=temp
                    else:
                        temp=info(input_port,packet[0].src)
                        list_info.append(temp)

                for intf in my_interfaces:
                    if input_port != intf.name:
                        log_debug ("Flooding packet {} to {}".format(packet, intf.name))
                        net.send_packet(intf.name, packet)
                        log_info ("boardcast packet from {} to {}".format(input_port, intf.name))
            else:
                flag=0
                for i in range(len(list_info)):
                    if list_info[i].address== packet[0].src:
                        flag=1
                        if list_info[i].port != input_port:
                            list_info[i].port = input_port
                        break
                if flag==0:
                    if len(list_info) >= max_len:
                        for i in range(1,len(list_info)):
                            list_info[i-1]=list_info[i]
                        temp=info(input_port,packet[0].src)
                        list_info[len(list_info)-1]=temp
                    else:
                        temp=info(input_port,packet[0].src)
                        list_info.append(temp)

                
                send_flag=0
                for i in range(len(list_info)):
                    if list_info[i].address == packet[0].dst:
                        net.send_packet(list_info[i].port, packet)
                        log_info ("find port {} of address {}".format(list_info[i].port,packet[0].dst))
                        send_flag=1
                        temp_info = list_info[i]
                        del(list_info[i])
                        list_info.append(temp_info)
                        break
            
                
                if send_flag!=1:
                    log_info("didn't find port")
                    for intf in my_interfaces:
                        if input_port != intf.name:
                            log_debug ("Flooding packet {} to {}".format(packet, intf.name))   
                            net.send_packet(intf.name, packet)
                            log_info ("didnt find packet from {} to {}".format(input_port, intf.name))
                            

    net.shutdown()