#created by SamJ
#github:github.com/BDeMo
#2019-3-5- 21:19:40

import socket
import threading
import sys
import time

import networkHelper.NetworkStatus as status
import networkHelper.tricks as tricks

class sThreadPool():
    def __init__(self, port, size):
        self.port = port
        self.size = size
        self.workers = {};

    class MultiServerThread(threading.Thread):
        def __init__(self, pool, workers, scs, addr, id=None, name=None):
            threading.Thread.__init__(self)
            if id == None:
                self.id = time.time()
            if name == None:
                self.name = time.ctime(time.time())
            workers[self.id] = self
            self.pool = pool
            self.scs = scs
            self.addr = addr
            self.counter = 0

        def __del__(self):
            if self.id in self.pool.workers:
                del self.pool.workers[self.id]
            self.scs.close()

        def run(self):
            self.pool.do(self.scs)
            self.__del__()

    def start(self):
        try:
            self.sServer = socket.socket()
            self.sServer.bind((tricks.get_host_ip(), self.port))
            self.sServer.listen(self.size)
            while True:
                scs, addr= self.sServer.accept()
                if not len(self.workers) > int(self.size):
                    newThread = sThreadPool.MultiServerThread(self, self.workers, scs, addr)
                    scs.send(status.ConnectionSuccess)
                    newThread.start()
                else:
                    scs.send(status.FullPoolRejection)
                    scs.close()
        finally:
            self.close()

    def close(self):
        self.sServer.send(status.ReactorClosed)
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
    # if len(sys.argv) > 1:
    #     pass;
    # else:
    #     print('arg1: port, arg2: size.')
    #     exit(1)
    # port = int(sys.argv[1])
    # size = int(sys.argv[2])
    port = 55667
    size = 10
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