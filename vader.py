from multiprocessing import Semaphore
from socket import *
from threading import Thread
import socket
import sys, signal, time, optparse

screenLock = Semaphore(value=1)


def main():
    parser = optparse.OptionParser('Como usar scann.py -H' + ' <target host> -p <target port')
    parser.add_option('-H', dest='tgtHost', type='string', help='ingrese el host')
    parser.add_option('-p', dest='tgtPort', type='string', help='ingrese el puerto')
    parser.add_option('-t', dest='threading', action='store_true', help='Ingrese los hilos a usar: -t 10')

    (options, args) = parser.parse_args()

    if options.tgtHost is None or options.tgtPort is None:
        print(parser.usage)
        exit(0)

    tgt_ports = list(map(int, filter(None, map(lambda p: p.strip(), options.tgtPort.split(",")))))
    portScan(options.tgtHost, tgt_ports, options.threading)


def connScan(tgtHost, tgtPorts):
    connSKT = None

    try:
        connSKT = socket(AF_INET, SOCK_STREAM)
        connSKT.connect((tgtHost, tgtPorts))
        connSKT.send('Dalton was here\r\n')
        results = connSKT.recv(100)
        screenLock.acquire()

        print(f"[+]%d tcp open {tgtHost}{tgtPorts}")
        print("[+]" + str(results))

    except Exception:
        screenLock.acquire()
        print(f"[-]%d tcp closed {tgtHost}")
    finally:
        screenLock.release()
        if connSKT:
            connSKT.close()


def portScan(tgtHost, tgtPorts, threading=False):
    
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print(f"[-] Cannot resolve : Unknown host {tgtIP}")
        return

    try:
        tgtName = gethostbyaddr(tgtIP)
        print(f"\n[+] Scan Result for: {tgtName[0]}")
    except:
        print(f"\n Scan Result for: {tgtIP}")

    setdefaulttimeout(1)
    for Port in tgtPorts:
        print(f"[+] Escaneando el host {tgtHost}:{tgtPorts}")
        if threading:
            t = Thread(target=connScan, args=(tgtHost, int(Port)))
            t.start()
        else:
            connScan(tgtHost, tgtPorts)


def banner():
    banner = """
     _    __          __             _____                      
    | |  / /___ _____/ /__  _____   / ___/_________ _____  ____ 
    | | / / __ `/ __  / _ \/ ___/   \__ \/ ___/ __ `/ __ \/ __ \/
    | |/ / /_/ / /_/ /  __/ /      ___/ / /__/ /_/ / / / / / / /
    |___/\__,_/\__,_/\___/_/      /____/\___/\__,_/_/ /_/_/ /_/ 
                                                                 ScannerPort: by D4lt0x6e
    """
    print(banner)

    print('< Happy Hacking ! >')
    print('    \    ^ __ ^    ')
    print('     \   ( oo ) \_______')
    print('         ( __ ) \        ) \/\/')
    print('             ||----w || ||  ')

    


if __name__ == '__main__':
    banner()
    print("")
    main()


                  
                                                            