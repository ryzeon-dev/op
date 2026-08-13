import sys
import os
from core import mapPids, scanProto

VERSION = '2.1.0'

if __name__ == '__main__':
    args = sys.argv[1:]

    if 'help' in args:
        print('op: Open Ports')
        print('usage: op [ARGS]\n')
        print('args:')
        print('    help       Show this message and exit')
        print('    tcp        Only show TCP open ports')
        print('    udp        Only show UDP open ports')
        print('    version    Show version and exit')
        print('\nin absence of arguments, both TCP and UDP will be shown')
        print('run as root to obtain pid and process name for every listening port')
        sys.exit(0)

    if 'version' in args:
        print(f'op v{VERSION}')
        sys.exit(0)
    
    elif 'tcp' in args:
        args.remove('tcp')

        showUdp = False 
        showTcp = True

    elif 'udp' in args:
        args.remove('udp')

        showTcp = False 
        showUdp = True 

    else:
        showUdp = True 
        showTcp = True

    if args:
        print('Invalid argument(s). Pass `help` as argument to get help')
        sys.exit(1)
    
    if os.getuid():
        print('PROTO ','ADDRESS'.ljust(15), ':', 'PORT')

    tcpMap = scanProto('tcp', '0A')
    udpMap = scanProto('udp', '07')

    if showTcp and os.geteuid():
        entries = list(tcpMap.values())
        entries = sorted(entries, key=lambda x: int(x[1]))

        for entry in entries:
            address, port = entry
            print(f'TCP   {address:15} : {port}')


    if showUdp and os.getuid():
        entries = list(udpMap.values())
        entries = sorted(entries, key=lambda x: int(x[1]))

        for entry in entries:
            address, port = entry
            print(f'UDP   {address:15} : {port}')

    if os.getuid():
        sys.exit(0)

    tcpLines, udpLines = mapPids(tcpMap, udpMap)
    print('PROTO  ' + 'ADDRESS'.ljust(15), ':', 'PORT'.ljust(5), '   PID',  '->', 'NAME')

    if showTcp:
        for entry in sorted(tcpLines, key=lambda x: int(x[1])):
            address, port, pid, processName = entry
            print(f'TCP    {address:15} : {port:5} {pid:6} -> {processName:6}')

    if showUdp:
        for entry in sorted(udpLines, key=lambda x: int(x[1])):
            address, port, pid, processName = entry
            print(f'UDP    {address:15} : {port:5} {pid:6} -> {processName:6}')