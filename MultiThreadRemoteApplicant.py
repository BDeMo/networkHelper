#created by SamJ
#github:github.com/BDeMo
#2019-3-6- 12:19:50

import socket
import sys
import threading
import time

import networkHelper.systemInfo as sysinfo

class sThreadPool():

    def __init__(self, ip, port, size):
        self.ip = ip
        self.port = port
        self.size = size
        self.id = time.time()
        self.workers = {}
        self.eOn = False
        self.started = False
        self.fstop = False

    class sThread(threading.Thread):
        def __init__(self, pool, workers, scs, addr, port, lock, id=None, name=None):
            threading.Thread.__init__(self)
            if id == None:
                self.id = time.time()
            if name == None:
                self.name = 'conTo:: ' + str(addr)
            self.pool = pool
            self.scs = scs
            self.addr = addr
            self.port = port
            self.lock = lock
            self.counter = 0
            workers[self.id] = self
            self.pool.workersip[self.addr] = self

        def __del__(self):
            if self.id in self.pool.workers:
                del self.pool.workers[self.id]
            self.scs.close()

        def stop(self):
            self.__del__()

        def run(self):
            while True:
                if self.pool.eOn:
                    self.lock.acquire()
                    self.pool.eOn = False
                    self.lock.release()
                    self.pool.do(self.scs, self.id)

    def start(self):
        try:
            if not self.started:
                self.lock = threading.Lock()
                for i in range(self.size):
                    scs = socket.socket()
                    scs.connect(self.ip, self.port)
                    newThread = sThreadPool.sThread(self, self.workers, scs, self.ip, self.port, self.lock)
                    newThread.start()
                while len(self.workers) <= 0 and not self.fstop:
                    pass
        finally:
            for wkr in self.workers:
                wkr.stop()

    def onEvent(self):
        self.lock.acquire()
        self.eOn = True
        self.lock.release()

    def stopAll(self):
        if self.started:
            self.fstop = True

    def do(self, socket, *args, **kwargs):
        pass

    def dispatch(self):
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

#implement example
class myThreadPool(sThreadPool):
    def __init__(self, ip, port, size):
        sThreadPool.__init__(self, ip, port, size)

    def do(self, socket, *args):
        print(socket.recv(1024))
        if args[0] in self.workers:
            self.workers[args[0]].stop()

#implement __main__
if __name__ == '__main__':
    try:
        ip = sysinfo.host_ipv4()
        port = 55667
        size = 10
        sysinfo.getOption()
        if sysinfo.ip != None:
            ip = sysinfo.ip
        if sysinfo.port != None:
            port = sysinfo.port
        if sysinfo.port != None:
            size = sysinfo.size
        tp = myThreadPool(ip, port, size)
        for i in range(size):
            tp.onEvent()
    finally:
        tp.stopAll()