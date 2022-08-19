import optparse 
import socket
from  socket import *


def main():
    parser = optparse.OptionParser('usage %prog -H' + '<target host> -p <target port')

    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')

    parser.add_option('-p', dest='tgtPort', type='int', help='specify target port')

    (options, args) = parser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = options.tgtPort

    if (tgtHost == None) |(tgtPorts == None):
        print(parser.usage)
        exit(0)

    portScan(tgtHost, tgtPorts)


def connScan(tgtHost, tgtPorts):
    try:
        connSKT = socket(AF_INET, SOCK_STREAM)

        connSKT.connect((tgtHost, tgtPorts))
        
        connSKT.send('Violent Python\r\n')
        results = connSKT.recv(100)

        print("[+]%d tcp open"%tgtPorts)
        print("[+]" + str(results))

        connSKT.close()
    except:
        print("[-]%d tcp closed"%tgtHost)


def portScan(tgtHost, tgtPorts):
    
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host"%tgtHost)

        return

    try:
        tgtName = gethostbyaddr(tgtIP)
        print("\n[+] Scan Result for: " + tgtName[0])
    except:

        print("\n Scan Result for: " + tgtIP)

    setdefaulttimeout(1)

    for tgtPort in tgtPorts:
        print("Scanning port" + tgtPort)
        connScan(tgtHost, int(tgtPort))


if __name__ == '__main__':
    main()


