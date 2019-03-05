import socket
import sys

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
    if len(sys.argv) > 1:
        pass
    else:
        print('arg1: addr, arg2: port')
        exit(1);
        try:
            scc = socket.socket()
            scc.connect((sys.argv[1], int(sys.argv[2])))
            print(scc.recv(1024))
        finally:
            scc.close()