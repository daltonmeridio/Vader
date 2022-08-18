import optparse 
from  socket import *

parser = optparse.OptionParser('usage %prog -H' + '<target host> -p <target port')

parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')

parser.add_option('-p', dest='tgtPort', type='int', help='specify target port')

(options, args) = parser.parse_args()

tgtHost = options.tgtHost
tgtPort = options.tgtPort

if (tgtHost == None) |(tgtPort == None):
    print(parser.usage)
exit(0)

def connScan(tgtHost, tgtPort):
    try:
        connSKT = socket(AF_INET, SOCK_STREAM)

        connSKT.connect((tgtHost, tgtPort))

        print("[+]%d tcp open"%tgtPort)

        connSKT.close()
    except:
        print("[-]%d tcp closed"%tgtHost)


def portScan(tgtHost, tgtPorts):
    
    try:
        tgtIP = gethostbyename(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host"%tgtHost)

    return

    try:
        tgtNanme = gethostbyaddr(tgtIP)
        print("\n[+] Scan Result for: " + tgtName[0])
    except:

        print("\n Scan Result for: " + tgtIP)

    setdefaulttimeout(1)

    for tgtPort in tgtPorts:
        print("Scanning port" + tgtPort)
        connScan(tgtHost, int(tgtPort))
