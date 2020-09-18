'''
Ethernet learning switch in Python.

Note that this file currently has the code to implement a "hub"
in it, not a learning switch.  (I.e., it's currently a switch
that doesn't learn.)
'''
from switchyard.lib.userlib import *

def main(net):
    boardcast_addr="ff:ff:ff:ff:ff:ff"
    my_interfaces = net.interfaces() 
    mymacs = [intf.ethaddr for intf in my_interfaces]
    list_port=[]
    list_address=[]
    while True:
        try:
            timestamp,input_port,packet = net.recv_packet()
        except NoPackets:
            continue
        except Shutdown:
            return     
             
        print("test info follows")
        for i in list_address:
            print(i)
        for i in list_port:
            print(i)
        print("test info end")

        log_debug ("In {} received packet {} on {}".format(net.name, packet, input_port))

        log_info ("In {} received packet {} on {}".format(net.name, packet, input_port))

        if packet[0].dst in mymacs:
            log_debug ("Packet intended for me")
        else:
            if packet[0].dst == boardcast_addr:
                if input_port in list_port:
                    print("boardcast src port in list")
                else:
                    print("boardcast src port not in list")
                    list_port.append(input_port)
                    list_address.append(packet[0].src)
                for intf in my_interfaces:
                    if input_port != intf.name:
                        log_debug ("Flooding packet {} to {}".format(packet, intf.name))
                        net.send_packet(intf.name, packet)
                        log_info ("boardcast packet from {} to {}".format(input_port, intf.name))
            else:
                if input_port in list_port:
                    print("src port in list")
                else:
                    print("src port not in list")
                    list_port.append(input_port)
                    list_address.append(packet[0].src)
                index=0
                send_flag=0
                for address in list_address:
                    if address==packet[0].dst:
                        net.send_packet(list_port[index], packet)
                        log_info ("find port {} of address {}".format(list_port[index],packet[0].dst))
                        send_flag=1
                        break
                    index+=1
                if send_flag!=1:
                    print("didn't find port")
                    for intf in my_interfaces:
                        if input_port != intf.name:
                            log_debug ("Flooding packet {} to {}".format(packet, intf.name))   
                            net.send_packet(intf.name, packet)
                            log_info ("didnt find packet from {} to {}".format(input_port, intf.name))
                            

    net.shutdown()