#created by SamJ
#github:github.com/BDeMo
#2019-3-6- 12:19:50

import socket
import sys
import threading
import time

import networkHelper.systemInfo as sysinfo

class sThreadPool():
    def __init__(self, pool, workers, scs, addr, id=None, name=None):
        threading.Thread.__init__(self)
        if id == None:
            self.id = time.time()
        if name == None:
            self.name = 'conTo:: ' + str(addr)
        self.pool = pool
        self.scs = scs
        self.addr = addr
        self.counter = 0
        workers[self.id] = self
        self.pool.workersip[self.addr] = self
        self.eOn = False

    class sThread(threading.Thread):
        def __init__(self, pool):
            self.pool = pool

        def __del__(self):
            if self.id in self.pool.workers:
                del self.pool.workers[self.id]
            if self.addr in self.pool.workersip:
                del self.pool.workersip[self.addr]
            self.scs.close()

        def run(self):
            while True:
                if self.pool.eOn:
                    self.pool.eOn = False
                    self.pool.do()

    def onEvent(self):
        eOn = True

    def do(self):
        pass



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