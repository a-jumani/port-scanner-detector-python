# port-scanner-detector-python
I've built a port scanner, a detector and an evader.

**Development Environment:** Python 2.7 on Sublime

**OS:** Ubuntu 16.04 LTS

## Port Scanner
PortScan probes all 2**16 TCP ports on a targeted host and reports the ports that accept connections. It reports both the port number and the service that normally runs on that port.

Usage: ``python PortScanner.py target``

## Port Scanner Detector
Detects and reports presence of a scanner if connection attempts were made to ``CON`` or more consecutive ports within a ``TIME`` seconds window.

Usage: ``[sudo] python PortSDetect.py``

## Port Scanner Detector Evader
Evades the port scanner detector implemented here.

Usage: ``python PortSDEvader.py target``
