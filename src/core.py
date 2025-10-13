import os
import re
from subprocess import getoutput

def decodeAddress(address):
    return '.'.join(( str(int(address[6:], 16)), str(int(address[4:6], 16)), str(int(address[2:4], 16)), str(int(address[:2], 16))))

def unpackLine(line):
    splitted = line.split(' ')

    while '' in splitted:
        splitted.remove('')

    localPair = splitted[1].split(':')
    listenAddress = decodeAddress(localPair[0])
    listenPort = str(int(localPair[1], 16))

    inode = splitted[9].strip()
    return listenAddress, listenPort, inode

def scanTcp():
    tcpMap = {}

    with open('/proc/net/tcp', 'r') as file:
        tcp = file.read()

    for line in tcp.split('\n'):
        if not line or line.strip().split(' ')[3] != '0A':
            continue

        address, port, inode = unpackLine(line.strip())
        if os.getuid():
            print(f'TCP    {address.ljust(15)} : {port}')

        else:
            tcpMap[inode] = [address, port]

    return tcpMap

def scanUdp():
    udpMap = {}

    with open('/proc/net/udp', 'r') as file:
        udp = file.read()

    for line in udp.split('\n'):
        if not line or line.strip().split(' ')[3] != '07':
            continue

        address, port, inode = unpackLine(line.strip())
        if os.getuid():
            print(f'UDP    {address.ljust(15)} : {port}')

        else:
            udpMap[inode] = [address, port]

    return udpMap

def mapPids(tcpMap, udpMap):
    for element in os.listdir('/proc'):
        if not re.fullmatch('^[0-9]+$', element):
            continue

        pid = element
        name = getoutput(f'cat /proc/{pid}/status | grep Name').replace('Name:', '').strip()

        pidFdPath = os.path.join('/proc', pid, 'fd')
        fileDescriptors = os.listdir(pidFdPath)

        for fd in fileDescriptors:
            fdPath = os.path.join(pidFdPath, fd)

            if not os.path.islink(fdPath):
                continue

            linkContent = os.readlink(fdPath)
            if not re.fullmatch(r'^socket:\[\d+\]$', linkContent):
                continue

            inode = linkContent.replace('socket:[', '').replace(']', '').strip()

            if inode in tcpMap:
                inodeData = tcpMap[inode]
                print(f'TCP    {inodeData[0].ljust(15)} : {inodeData[1].ljust(5)} {pid.rjust(6)} -> {name.ljust(6)}')

            elif inode in udpMap:
                inodeData = udpMap[inode]
                print(f'UDP    {inodeData[0].ljust(15)} : {inodeData[1].ljust(5)} {pid.rjust(6)} -> {name.ljust(6)}')

    return tcpMap, udpMap