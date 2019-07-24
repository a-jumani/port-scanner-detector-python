import Consecutive
import dpkt
import ipaddress
import pcap
import socket
import time

MY_IP = ''
TIME = 5
CON = 15
MIN_PORT, MAX_PORT = 0, 2**16 - 1
TRACKER = {}

def self_ip():
    '''
    get IP of this machine

    returns:
        None
    raises:
        socket.error
        AssertionError
    '''
    global MY_IP

    # connect to any address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))

    # extract IP
    MY_IP = s.getsockname()[0]
    s.close()

def track(src_ip, dst_port):
    '''
    keep track of incoming pkts to detect port scanners

    params:
        src_ip          source ip
        dst_port        port on this machine contacted
    returns:
        None
    '''

    # new source
    if src_ip not in TRACKER:
        ports_visited = Consecutive.Consecutive()
        ports_visited.insert(dst_port, CON, TIME, MIN_PORT, MAX_PORT)
        TRACKER[src_ip] = ports_visited

    # source seen before
    else:
        # check if this machine is being port scanned
        if TRACKER[src_ip].insert(dst_port, CON, TIME, MIN_PORT, MAX_PORT):
            print "Scanner detected. The scanner originated from host {0:s}.".format(src_ip)

def parse_pkt(pkt):
    '''
    parse pkt and hand it off to the tracker an inbound pkt

    params:
        pkt<buffer>     packet given by pcap.pcap
    returns:
        None
    '''

    # extract ip
    eth = dpkt.ethernet.Ethernet(pkt)
    ip = eth.data
    src_ip = ipaddress.IPv4Address(ip.src)
    dst_ip = ipaddress.IPv4Address(ip.dst)

    # ignore outgoing packet
    if str(src_ip) == MY_IP:
       return

    # extract port
    dst_port = ip.data.dport

    # send to tracker
    track(src_ip, dst_port)

if __name__ == '__main__':

    # get my IP
    try:
        self_ip()
    except socket.error, e:
        print "Could not resolve this machine's IP address. Error: {0:s}".format(str(e))
        sys.exit(1)

    # set up a listener for TCP traffic
    pc = pcap.pcap(promisc=False, immediate=True)
    pc.setfilter('tcp')
    print "Listening on {0:s}: {1:s}".format(pc.name, pc.filter)

    # capture packets
    for _, pkt in pc:
        parse_pkt(pkt)