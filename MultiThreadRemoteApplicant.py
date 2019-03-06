#created by SamJ
#github:github.com/BDeMo
#2019-3-6- 12:19:50

import socket
import sys

import networkHelper.systemInfo as sysinfo

#example
def doInput(scc):
    try:
        while True:
            str = input()
            scc.send(bytes(str, encoding='utf-8'))
            if str == 'Q' or str == 'q':
                break
    finally:
        scc.close()

# if __name__ == '__main__':
if __name__ == '__main__':
    ip = sysinfo.host_ipv4()
    port = 55667
    sysinfo.getOption()
    if sysinfo.ip != None:
        ip = sysinfo.ip
    if sysinfo.port != None:
        port = sysinfo.port
    try:
        scc = socket.socket()
        scc.connect((ip, port))
        print(scc.recv(1024))
    finally:
        scc.close()