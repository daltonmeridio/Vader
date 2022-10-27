from multiprocessing import Semaphore
from socket import *
from threading import Thread
import socket
import optparse

screenLock = Semaphore(value=1)


def main():
    parser = optparse.OptionParser('Uso: vader.py -H' + ' <target ip> -p <target port>')
    parser.add_option('-H', dest='Target_IP', type='string', help='ingrese el host')
    parser.add_option('-p', dest='Target_Port', type='string', help='ingrese el puerto')
    parser.add_option('-t', dest='threading', action='store_true', help='Ingrese los hilos a usar: -t 10')

    (options, args) = parser.parse_args()

    if options.Target_IP is None or options.target_Port is None:
        print(parser.usage)
        exit(0)

    target_ports = list(map(int, filter(None, map(lambda p: p.strip(), options.Target_Port.split(",")))))
    portScan(options.Target_IP, target_ports, options.threading)


def connScan(Target_IP, Target_Port):
    connSKT = None

    try:
        connSKT = socket(AF_INET, SOCK_STREAM)
        connSKT.connect((Target_IP, Target_Port))
        connSKT.send('Dalton was here\r\n')
        results = connSKT.recv(100)
        screenLock.acquire()

        print(f"[+]%d tcp open {Target_IP}{Target_Port}")
        print("[+]" + str(results))

    except Exception:
        screenLock.acquire()
        print(f"[-]%d tcp closed {Target_IP}")
    finally:
        screenLock.release()
        if connSKT:
            connSKT.close()


def portScan(Target_IP, Target_Port, threading=False):
    
    try:
        t_IP = gethostbyname(Target_IP)
    except:
        print(f"[-] Cannot resolve : Unknown host {t_IP}")
        return

    try:
        T_Name = gethostbyaddr(t_IP)
        print(f"\n[+] Scan Result for: {T_Name[0]}")
    except:
        print(f"\n Scan Result for: {t_IP}")

    setdefaulttimeout(1)
    for Port in Target_IP:
        print(f"[+] Escaneando el host {Target_IP}:{Target_Port}")
        if threading:
            t = Thread(target=connScan, args=(Target_IP, int(Port)))
            t.start()
        else:
            connScan(Target_IP, Target_Port)


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
    print('     \   ( oo ) \________\/\/')
    print('         ( __ ) \        )  ')
    print('             ||----w || ||  ')

    


if __name__ == '__main__':
    banner()
    print("")
    main()


                  
                                                            