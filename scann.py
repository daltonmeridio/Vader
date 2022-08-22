from multiprocessing import Semaphore
import optparse 
import socket
from  socket import *
from threading import Thread
import signal
import sys

def main():
    parser = optparse.OptionParser('Como usar %prog -H' + '<target host> -p <target port')

    parser.add_option('-H', dest='tgtHost', type='string', help='ingrese el host')

    parser.add_option('-p', dest='tgtPort', type='string', help='ingrese el puerto')

    (options, args) = parser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = options.tgtPort

    if (tgtHost == None) |(tgtPorts == None):
        print(parser.usage)
        exit(0)

    portScan(tgtHost, tgtPorts)

screenLock = Semaphore(value=1)


#def nmapScan(tgtHost, tgtPort):
#   nmScan = nmap.PortScanner()
#   nmScan.scan(tgtHost, tgtPort)
#   state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
#
#   print("[*]" + tgtHost + "tcp/" + tgtPort + "" + state)


def connScan(tgtHost, tgtPorts):
    try:
        connSKT = socket(AF_INET, SOCK_STREAM)

        connSKT.connect((tgtHost, tgtPorts))
        
        connSKT.send('Violent Python\r\n')
        results = connSKT.recv(100)

        screenLock.acquire()

        print("[+]%d tcp open"%tgtPorts)
        print("[+]" + str(results))

    except:
        screenLock.acquire()

        print("[-]%d tcp closed"%tgtHost)

    finally:
        screenLock.acquire()
        connSKT.close()


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

    for Port in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(Port)))
        t.start()


def sigint_handler(signal, frame):
    print ('KeyboardInterrupt is caught')
    sys.exit(0)
    signal.signal(signal.SIGINT, sigint_handler)



def banner():
    banner = """
                  ___          ___      ___     
     _____       /\  \        /\__\    /\__\    
    /::\  \     /::\  \      /:/ _/_  /:/ _/_   
   /:/\:\  \   /:/\:\  \    /:/ /\__\/:/ /\__\  
  /:/  \:\__\ /:/ /::\  \  /:/ /:/  /:/ /:/  /  
 /:/__/ \:|__/:/_/:/\:\__\/:/_/:/  /:/_/:/  /   
 \:\  \ /:/  |:\/:/  \/__/\:\/:/  /\:\/:/  /    
  \:\  /:/  / \::/__/      \::/__/  \::/__/     
   \:\/:/  /   \:\  \       \:\  \   \:\  \     
    \::/  /     \:\__\       \:\__\   \:\__\    
     \/__/       \/__/        \/__/    \/__/   ScannerPort: by D4lt0x6e
    """
    print(banner)


if __name__ == '__main__':
    banner()
    main()


