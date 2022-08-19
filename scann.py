from multiprocessing import Semaphore
import optparse 
import socket
from  socket import *
from threading import Thread


def main():
    parser = optparse.OptionParser('usage %prog -H' + '<target host> -p <target port')

    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')

    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port')

    (options, args) = parser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = options.tgtPort

    if (tgtHost == None) |(tgtPorts == None):
        print(parser.usage)
        exit(0)

    portScan(tgtHost, tgtPorts)

screenLock = Semaphore(value=1)


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


