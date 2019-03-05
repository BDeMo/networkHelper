#created by SamJ
#github:github.com/BDeMo
#2019-3-5- 21:19:40
import socket

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# print(get_host_ip())