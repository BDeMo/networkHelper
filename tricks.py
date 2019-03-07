#created by SamJ
#github:github.com/BDeMo
#2019-3-5- 21:19:40
import socket
import threading
import time

localLock = threading.Lock()
blockq = {}

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def mutex_p(mutex, lock):
    if lock not in blockq:
        blockq[lock]=[]
    if mutex <= 0:
        thrd = threading.current_thread()
        blockq[lock].append(thrd)
        while thrd in blockq[lock]:
            pass

def mutex_v(mutex, lock):
    if lock not in blockq:
        blockq[lock]=[]
    if mutex <= 0:
        while len(blockq[lock])<=0:
            pass
        blockq[lock].pop()

if __name__ == '__main__':
    print(get_host_ip())