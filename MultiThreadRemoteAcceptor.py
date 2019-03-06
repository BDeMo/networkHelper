#created by SamJ
#github:github.com/BDeMo
#2019-3-5- 21:19:40

import socket
import threading
import time

import networkHelper.protocol as prtcl
import networkHelper.systemInfo as sysinfo

class sThreadPool():
    def __init__(self, port, size):
        self.port = port
        self.size = size
        self.id = time.time()
        self.workersip = {}
        self.workers = {}

    class sThread(threading.Thread):
        def __init__(self, pool, workers, scs, addr, id=None, name=None):
            threading.Thread.__init__(self)
            if id == None:
                self.id = time.time()
            if name == None:
                self.name = 'conTo:: '+str(addr)
            self.pool = pool
            self.scs = scs
            self.addr = addr
            self.counter = 0
            workers[self.id] = self
            self.pool.workersip[self.addr] = self

        def __del__(self):
            if self.id in self.pool.workers:
                del self.pool.workers[self.id]
            if self.addr in self.pool.workersip:
                del self.pool.workersip[self.addr]
            self.scs.close()

        def run(self):
            self.pool.do(self.scs)
            self.__del__()

    def start(self):
        try:
            self.sServer = socket.socket()
            self.sServer.bind((sysinfo.host_ipv4(sysinfo), self.port))
            self.sServer.listen(self.size)
            while True:
                scs, addr= self.sServer.accept()
                if len(self.workers) < int(self.size):
                    newThread = sThreadPool.sThread(self, self.workers, scs, addr)
                    scs.send(prtcl.preTran({prtcl.StatusCode:prtcl.ConnectionSuccess}))
                    newThread.start()
                else:
                    scs.send(prtcl.preTran({prtcl.StatusCode:prtcl.FullPullRejection}))
                    scs.close()
        finally:
            self.close()

    def close(self):
        self.sServer.send(prtcl.preTran({prtcl.StatusCode:prtcl.ReactorClosed}))
        self.sServer.close()

    #the function you need to override
    def do(self, socket):
        pass

#implement example
class myThreadPool(sThreadPool):

    def __init__(self, port, size):
        sThreadPool.__init__(self, port, size)

    def do(self, socket):
        try:
            socket.send(bytes('connected :'+time.ctime(time.time()), encoding='utf-8'))
            print(self.workers)
        finally:
            socket.close()

#implement __main__
if __name__ == '__main__':
    port = 55667
    size = 0
    sysinfo.getOption(sysinfo);
    if sysinfo.port != None:
        port = sysinfo.port
    if sysinfo.size != None:
        size = sysinfo.size
    tp = myThreadPool(port, size)
    tp.start()
    # try:
    #     sServer = socket.socket()
    #     sServer.bind((get_host_ip(), port))
    #     sServer.listen(size)
    #     while True:
    #         scs, addr= sServer.accept()
    #         if not len(workers) > int(size):
    #             newThread = MultiServerThread(workers, scs, addr)
    #             newThread.start()
    # finally:
    #     sServer.close()