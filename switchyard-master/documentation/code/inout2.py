from switchyard.lib.userlib import *

def main(net):
    # below, recvdata is a namedtuple
    recvdata = net.recv_packet()
    print ("At {}, received {} on {}".format(
        recvdata.timestamp, recvdata.packet, recvdata.input_port))

    # alternatively, the above line could use indexing, although
    # readability suffers:
    #    recvdata[0], recvdata[2], recvdata[1]))
    
    net.send_packet(recvdata.input_port, recvdata.packet)

    # likewise, the above line could be written using indexing
    # but, again, readability suffers:
    # net.send_packet(recvdata[1], recvdata[2])
