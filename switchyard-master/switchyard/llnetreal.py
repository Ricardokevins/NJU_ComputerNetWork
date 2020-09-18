import sys
import argparse
import os
import signal
import re
import subprocess
from time import time as now
import threading
import textwrap
from queue import Queue,Empty
import socket

from psutil import net_if_addrs

from .lib.address import *
from .lib.packet import *
from .lib.exceptions import Shutdown, NoPackets
from .lib.interface import Interface, InterfaceType
from .lib.logging import setup_logging, log_info, log_debug, log_warn, log_failure
from .importcode import import_or_die
from .textcolor import *

from .pcapffi import *
from .llnetbase import LLNetBase, ReceivedPacket, _start_usercode

_dlt_to_decoder = {}
_dlt_to_decoder[Dlt.DLT_EN10MB] = lambda raw: Packet(raw, first_header=Ethernet)
_dlt_to_decoder[Dlt.DLT_NULL] = lambda raw: Packet(raw, first_header=Null)

class LLNetReal(LLNetBase):
    '''
    A class that represents a collection of network devices
    on which packets can be received and sent.
    '''
    def __init__(self, devlist, name=None):
        LLNetBase.__init__(self)
        signal.signal(signal.SIGINT, self._sig_handler)
        signal.signal(signal.SIGTERM, self._sig_handler)
        signal.signal(signal.SIGHUP, self._sig_handler)
        signal.signal(signal.SIGUSR1, self._sig_handler)
        signal.signal(signal.SIGUSR2, self._sig_handler)

        self._devs = devlist 
        self._devinfo = self._assemble_devinfo()
        self._pcaps = {}
        self._localsend = {}
        self._pktqueue = Queue()
        self._threads = []
        self._make_pcaps()
        log_info("Using network devices: {}".format(' '.join(self._devs)))
        for devname, intf in self._devinfo.items():
            log_debug("{}: {}".format(devname, str(intf)))

        LLNetReal.running = True
        self._spawn_threads()

        if name:
            self._name = name
        else:
            self._name = socket.gethostname()

    @property
    def name(self):
        return self._name

    @property
    def testmode(self):
        return False

    def shutdown(self):
        '''
        Should be called by Switchyard user code when a network object is
        being shut down.  (This method cleans up internal threads and network
        interaction objects.)
        '''
        if not LLNetReal.running:
            return

        LLNetReal.running = False
        log_debug("Joining threads for shutdown")
        for t in self._threads:
            t.join()
        log_debug("Closing pcap devices")
        for devname,pdev in self._pcaps.items():
            pdev.close()
        for rdev in self._localsend.values():
            rdev.close()
        log_debug("Done cleaning up")

    def _spawn_threads(self):
        '''
        Internal method.  Creates threads to handle low-level
        network receive.
        '''
        for devname,pdev in self._pcaps.items():
            t = threading.Thread(target=LLNetReal._low_level_dispatch, args=(pdev, devname, self._pktqueue))
            t.start()
            self._threads.append(t)

    def _assemble_devinfo(self):
        '''
        Internal method.  Assemble information on each interface/
        device that we know about, i.e., its MAC address and configured
        IP address and prefix.
        '''
        devtype = {}
        for p in pcap_devices():
            if p.isloop:
                devtype[p.name] = InterfaceType.Loopback
            else:
                if sys.platform == 'linux':
                    st,output = subprocess.getstatusoutput(["iwconfig", p.name])
                    if "no wireless extensions" in output:
                        devtype[p.name] = InterfaceType.Wired
                    else:
                        devtype[p.name] = InterfaceType.Wireless
                elif sys.platform == 'darwin':
                    devtype[p.name] = InterfaceType.Unknown
                else:
                    devtype[p.name] = InterfaceType.Unknown

        devinfo = {}
        ifinfo = net_if_addrs()
        for devname in self._devs:
            ifaddrs = ifinfo.get(devname, None)
            if ifaddrs is None:
                log_warn("Address info for interface {} not found! (skipping)".format(devname))

            if sys.platform == 'darwin':
                layer2addrfam = socket.AddressFamily.AF_LINK
            elif sys.platform == 'linux':
                layer2addrfam = socket.AddressFamily.AF_PACKET
            else:
                raise RuntimeException("Platform not supported")

            macaddr = "00:00:00:00:00:00"
            ipaddr = mask = "0.0.0.0"
            for addrinfo in ifaddrs:
                if addrinfo.family == socket.AddressFamily.AF_INET:
                    ipaddr = IPv4Address(addrinfo.address)
                    mask = IPv4Address(addrinfo.netmask)
                elif addrinfo.family == layer2addrfam:
                    macaddr = EthAddr(addrinfo.address)

            ifnum = socket.if_nametoindex(devname)
            devinfo[devname] = Interface(devname, macaddr, ipaddr, netmask=mask, ifnum=ifnum, iftype=devtype[devname])
        return devinfo

    def _make_pcaps(self):
        '''
        Internal method.  Create libpcap devices
        for every network interface we care about and
        set them in non-blocking mode.
        '''
        self._pcaps = {}
        for devname,intf in self._devinfo.items():
            if intf.iftype == InterfaceType.Loopback:
                senddev = _RawSocket(devname, protocol=IPProtocol.UDP)
                self._localsend[devname] = senddev
            pdev = PcapLiveDevice(devname) 
            self._pcaps[devname] = pdev

    def _sig_handler(self, signum, stack):
        '''
        Handle process INT signal.
        '''
        log_debug("Got SIGINT.")
        if signum == signal.SIGINT:
            LLNetReal.running = False
            if self._pktqueue.qsize() == 0:
                # put dummy pkt in queue to unblock a 
                # possibly stuck user thread
                self._pktqueue.put( (None,None,None) )

    @staticmethod
    def _low_level_dispatch(pcapdev, devname, pktqueue):
        '''
        Thread entrypoint for doing low-level receive and dispatch
        for a single pcap device.
        '''
        while LLNetReal.running:
            # a non-zero timeout value is ok here; this is an
            # independent thread that handles input for this
            # one pcap device.  it throws any packets received
            # into the shared queue (which is read by the actual
            # user code)
            pktinfo = pcapdev.recv_packet(timeout=0.2)
            if pktinfo is None:
                continue
            pktqueue.put( (devname,pcapdev.dlt,pktinfo) )

        log_debug("Receiver thread for {} exiting".format(devname))
        stats = pcapdev.stats()
        log_debug("Final device statistics {}: {} received, {} dropped, {} dropped/if".format(devname, stats.ps_recv, stats.ps_drop, stats.ps_ifdrop))

    def recv_packet(self, timeout=None):
        '''
        Receive packets from any device on which one is available.
        Blocks until it receives a packet, unless a timeout value >=0
        is given.  Raises Shutdown exception when device(s) are shut 
        down (i.e., on a SIGINT to the process).  Raises NoPackets when 
        there are no packets that can be read.

        Returns a ReceivedPacket named tuple (timestamp, input_port, packet)
        '''
        while True:
            try:
                dev,dlt,pktinfo = self._pktqueue.get(timeout=timeout)
                if not LLNetReal.running:
                    break

                decoder = _dlt_to_decoder.get(dlt, None)
                if decoder is None:
                    log_warn("Received packet with unparseable encapsulation {}".format(dlt))
                    continue

                pkt = decoder(pktinfo.raw) 
                return ReceivedPacket(timestamp=pktinfo.timestamp, 
                    input_port=dev, packet=pkt)
            except Empty:
                if not LLNetReal.running:
                    raise Shutdown()
                raise NoPackets()
        raise Shutdown()

    def send_packet(self, dev, packet):
        '''
        Send a Switchyard Packet object on the given device 
        (string name of device).

        Raises ValueError if packet object isn't valid, or device
        name isn't recognized.
        '''
        if packet is None:
            raise ValueError("No packet object given to send_packet")
        if not isinstance(packet, Packet):
            raise ValueError("Object given to send_packet is not a Packet (it is: {})".format(type(packet)))
 
        intf = None
        if isinstance(dev, int):
           dev = self._lookup_devname(dev)

        if isinstance(dev, Interface):
            intf = dev
            dev = dev.name
        elif dev in self._devinfo:
            intf = self.interface_by_name(dev)
        else:
            raise ValueError("Unrecognized device name for packet send: {}".format(dev))

        if intf.iftype == InterfaceType.Loopback:
            pdev = self._localsend.get(dev, None)
            pdev.send_packet(packet)
        else:
            pdev = self._pcaps.get(dev, None)
            rawpkt = packet.to_bytes()
            log_debug("Sending packet on device {}: {}".format(dev, str(packet)))
            pdev.send_packet(rawpkt)

def main_real(usercode, netobj, options):
    '''
    Entrypoint function for non-test ("real") mode.  At this point
    we assume that we are running as root and have pcap module.
    '''
    usercode_entry_point = import_or_die(usercode, ('main', 'switchy_main'))
    if options.dryrun:
        log_info("Imported your code successfully.  Exiting dry run.")
        netobj.shutdown()
        return

    try:
        _start_usercode(usercode_entry_point, netobj, options.codearg)
    except Exception as e:
        import traceback

        log_failure("Exception while running your code: {}".format(e))
        message = '''{0}

This is the Switchyard equivalent of the blue screen of death.
Here (repeating what's above) is the failure that occurred:
'''.format('*'*60, textwrap.fill(str(e), 60))
        with red():
            print(message)
            traceback.print_exc(1)
            print('*'*60)

        if options.nohandle:
            raise 
            
        if not options.nopdb:
            print('''
I'm throwing you into the Python debugger (pdb) at the point of failure.
If you don't want pdb, use the --nopdb flag to avoid this fate.
''')
            import pdb
            pdb.post_mortem()
    else:
        netobj.shutdown()


class _RawSocket(object):
    '''
    Class to encapsulate a raw socket for use with the localhost interface.
    libpcap doesn't work for sending packets on localhost for some platforms
    (notably, Linux), so we use a raw socket instead for consistency.
    We implement the same set of methods as PcapLiveDevice (in .pcapffi)
    to make it quack like all other interfaces.
    '''
    def __init__(self, name, protocol=IPProtocol.ICMP):
        self._name = name
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, protocol)
        self._sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
        self._sock.setblocking(True)
        self._sent = self._recv = 0
        self._doswap = sys.platform == 'darwin'

    @staticmethod
    def set_bpf_filter_on_all_devices(filterstr):
        pass

    @property
    def dlt(self):
        return Dlt.DLT_NULL

    def recv_packet(self, timeout):
        if timeout is None or timeout < 0:
            timeout = None

        self._sock.settimeout(timeout)
        try:
            raw,addrinfo = self._sock.recvfrom(1500)
            xlen = len(raw)
            log_debug("{}: received {} bytes from {} on raw".format(self._name, xlen, addrinfo))
            return PcapPacket(now(), xlen, xlen, raw)
        except Exception as e:
            log_warn("{}: error receiving {}".format(self._name, str(e)))
            return None

    def send_packet(self, packet):
        n = packet.num_headers()
        if n == 0:
            raise PcapException("{}: packet doesn't have any headers".format(self._name))
        first = packet[0]
        if isinstance(first, (Null,Ethernet)):
            del packet[0]
            n -= 1
            if n == 0:
                raise PcapException("{}: packet doesn't have any headers besides Null".format(self._name))
        first = packet[0]
        if not isinstance(first, (IPv4,IPv6)):
            raise PcapException("{}: first header must be IPv4 or IPv6".format(self._name))

        raw = packet.to_bytes()
        port = 0
        if packet.has_header(UDP):
            port = packet[UDP].dst
        addr = (str(packet[0].dst), port)

        # everything in raw is in *network* byte order, but raw socket on
        # macos expects offset and length in *host* byte order.  yup, it's
        # byte-swapping time.  length is located at index 2 (length 2).
        # offset is located at index.  
        # for linux, offset should be in network byte order.  thanks a bunch.
        version = raw[0] >> 4
        if version == 4:
            if self._doswap:
                tlen = raw[2:4][::-1]
                offset = raw[6:8][::-1]
                raw = raw[:2] + tlen + raw[4:6] + offset + raw[8:]
        else:
            raise NotImplementedError("Can't handle IPv6 with localhost send yet.")

        sent = self._sock.sendto(raw, addr) # may raise exception
        if len(raw) != sent:
            raise PcapException("{}: only sent {} of {} bytes".format(self._name, sent, len(raw)))
        return True

    def close(self):
        self._sock.close()

    def stats(self):
        return PcapStats(self._recv, 0, 0)

    def set_filter(self, filterstr):
        pass
