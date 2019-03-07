#created by SamJ
#github:github.com/BDeMo
#2019-3-6- 12:19:50

import socket
import sys
import threading
import time

import networkHelper.tricks as tricks
import networkHelper.systemInfo as sysinfo

class sThreadPool():

    def __init__(self, ip, port, size, interval=1):
        self.ip = ip
        if isinstance(port, (str, float)):
            self.port = int(port)
        elif isinstance(port, int):
            self.port = port
        else:
            raise Exception('Error port')
        if isinstance(size, (str, float)):
            self.size = int(size)
        elif isinstance(size, int):
            self.size = size
        else:
            raise Exception('Error size')
        if isinstance(interval, (str, float)):
            self.interval = int(interval)
        elif isinstance(interval, int):
            self.interval = interval
        else:
            raise Exception('Error interval')
        self.id = time.time()
        self.workers = {}
        self.started = False
        self.fstop = False
        self.lock_counterEvent = threading.Lock()
        self.lock_counter = threading.Lock()
        self.counterEvent = 0
        self.counter = self.size
        # global counterEvent = 0
        # global counter = self.size

    class sThread(threading.Thread):
        def __init__(self, pool, scs, addr, port, id=None, name=None):
            threading.Thread.__init__(self)
            if id == None:
                self.id = time.time()
            if name == None:
                self.name = 'conTo:: ' + str(addr)
            self.pool = pool
            self.scs = scs
            self.addr = addr
            self.port = port
            self.pool.workers[self.id] = self

        def __del__(self):
            if self.id in self.pool.workers:
                del self.pool.workers[self.id]
                self.scs.close()

        def stop(self):
            self.__del__()

        def run(self):
            self.pool.counterEvent-=1
            tricks.mutex_p(self.pool.counterEvent, self.pool.lock_counterEvent)
            self.pool.do(self.scs, self.id)
            self.pool.counter+=1
            tricks.mutex_v(self.pool.counter, self.pool.lock_counter)
            time.sleep(self.pool.interval)
    # A bug in onEvent Function and sThread.run function about lock
    def start(self):
        try:
            if not self.started:
                for i in range(self.size):
                    scs = socket.socket()
                    scs.connect((self.ip, self.port))
                    newThread = sThreadPool.sThread(self, scs, self.ip, self.port)
                    newThread.start()
            time.sleep(interval)
            while len(self.workers) <= 0 and not self.fstop:
                pass
        except ConnectionRefusedError:
            raise  ConnectionRefusedError("refused by host"+self.ip)

    def onEvent(self):
        self.counter-=1
        tricks.mutex_p(self.counter, self.lock_counter)
        self.counterEvent+=1
        tricks.mutex_v(self.counterEvent, self.lock_counterEvent)

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
    def __init__(self, ip, port, size, interval):
        sThreadPool.__init__(self, ip, port, size, interval)

    def do(self, socket, *args):
        print(socket.recv(1024))
        socket.send(bytes('res ' + time.ctime(time.time()),encoding='utf-8'))
        # if args[0] in self.workers:
        #     self.workers[args[0]].stop()

#implement __main__
if __name__ == '__main__':
    tp = None
    interval = 0.5
    port = 55667
    size = 10
    try:
        ip = sysinfo.host_ipv4(sysinfo)
        sysinfo.getOption(sysinfo)
        if sysinfo.ip != None:
            ip = sysinfo.ip
        if sysinfo.port != None:
            port = sysinfo.port
        if sysinfo.size != None:
            size = int(sysinfo.size)
        if sysinfo.interval != None:
            interval = int(sysinfo.interval)
        tp = myThreadPool(ip, port, size, interval=interval)
        tp.start()
        for i in range(size):
            tp.onEvent()
    finally:
        if tp is not None:
            tp.stopAll()