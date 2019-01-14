import multiprocessing
import socket
import sys
import time

CONNECTION_TIMEOUT = 1.0    # timeout for connection establishment
NUM_CONC_SOCKETS = 40       # number of concurrent connections allowed
NUM_PORTS = 2**16           # check ports 0, 1, ... , NUM_PORTS - 1

def check_port(target, p):
    '''
    check if a port of a host is active

    params:
        target<str>     IP address of host
        p<int>          port number
    returns:
        p if connection was successful, -1 otherwise
    preconditions:
        p is between 0 and 65535, inclusive
    '''
    
    # create a socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(CONNECTION_TIMEOUT)
    except socket.error as e:
        print "socket creation failed for port {0:d}".format(p)
        return -1

    # try to connect
    status = s.connect_ex((target, p))
    s.close()

    # connection was successful
    if status == 0:
        return p

    # connection failed
    else:
        return -1

if __name__ == '__main__':

    # get target name
    try:
        target = socket.gethostbyname(sys.argv[1])
    except socket.gaierror:
        print "an error was encountered while resolving the host."
        sys.exit(1)

    # set up for multiprocessing
    pool = multiprocessing.Pool(processes=NUM_CONC_SOCKETS)
    
    # set up for measurement
    start = time.time()
    ports_open = 0
    
    # scan ports
    output = [pool.apply_async(check_port, args=(target, x)) for x in range(NUM_PORTS)]
    results = [p.get() for p in output]
    
    # record time taken
    end = time.time()
    time_taken = end - start
    
    # print results on open ports
    for i in (x for x in results if x != -1):
        try:
            print "{0:d}, {1:s}".format(i, socket.getservbyport(i, "tcp"))
        except:
            print "{0:d}, unknown service".format(i)
        ports_open += 1

    # print other results
    print "-------------------------------------------"
    print "Time taken: {0:.2f} s".format(time_taken)
    print "Ports open: {0:d}".format(ports_open)
    print "Scan rate: {0:.2f} ports/s".format(NUM_PORTS / time_taken)
