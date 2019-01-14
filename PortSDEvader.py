import multiprocessing
import PortScanner
import socket
import sys
import time

NUM_CONC_SOCKETS = 40       # number of concurrent connections allowed
NUM_PORTS = 2**16           # check ports 0, 1, ... , NUM_PORTS - 1
ESCAPE_CON = 15             # number of consecutive ports the scanning detector will report on

def mix_count(count, num):
    '''
    sequence S = range(count) such that consecutive numbers have gap of num;
    we restart the sequence from the lowest unused number of S when a sequence
    is exchausted; e.g.
    mix_count(10, 5) = [0, 5, 1, 6, 2, 7, 3, 8, 4, 9]
    mix_count(20, 3) = [0, 3, 6, 9, 12, 15, 18, 1, 4, 7, 10, 13, 16, 19, 2, 5, 8, 11, 14, 17]

    params:
        count<int>      to rearrange numbers in range(count)
        num<int>        gap
    returns:
        list of numbers
    '''
    return [i for x in range(num) for i in range(x, count, num)]    

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
    ports_to_scan = mix_count(NUM_PORTS, ESCAPE_CON)
    output = [pool.apply_async(PortScanner.check_port, args=(target, x)) for x in ports_to_scan]
    results = [p.get() for p in output]
    
    # record time taken
    end = time.time()
    time_taken = end - start
    
    # print results on ports open
    results.sort()
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
