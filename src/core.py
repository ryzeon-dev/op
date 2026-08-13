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

def scanProto(proto, flag):
    protoMap = {}
    with open(f'/proc/net/{proto}', 'r') as file:
        content = file.read()

    for line in content.split('\n'):
        if not line or line.strip().split(' ')[3] != flag:
            continue

        address, port, inode = unpackLine(line.strip())
        protoMap[inode] = [address, port]

    return protoMap

def mapPids(tcpMap, udpMap):
    tcpEntries = []
    udpEntries = []

    for element in os.listdir('/proc'):
        if not re.fullmatch('^[0-9]+$', element):
            continue

        pid = element
        name = getoutput(f'cat /proc/{pid}/status | grep Name').replace('Name:', '').strip()

        pidFdPath = os.path.join('/proc', pid, 'fd')

        try:
            fileDescriptors = os.listdir(pidFdPath)

        except:
            continue

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
                tcpEntries.append((inodeData[0], inodeData[1], pid, name))

            elif inode in udpMap:
                inodeData = udpMap[inode]
                udpEntries.append((inodeData[0], inodeData[1], pid, name))

    return tcpEntries, udpEntries