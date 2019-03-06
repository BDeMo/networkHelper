import sys
import os
import getopt

import networkHelper.tricks as tricks

address_IPv4 = None
OSinfo = None
port = None
ip = None
size = None

def host_ipv4(self):
    if self.address_IPv4 == None:
        address_IPv4 = tricks.get_host_ip()
    return address_IPv4

def OsInfo(self):
    if self.OSinfo == None:
        self.OSinfo = os.system('uname -a')
    return self.OSinfo

def usage():
    pass

def getOption(self):
    try:
        options, args = getopt.getopt(sys.argv[1:], "hp:i:s:", ["help", "ip=", "port=","size="])
    except getopt.GetoptError:
        sys.exit()
    for name, value in options:
        if name in ("-h", "--help"):
            usage()
        if name in ("-i", "--ip"):
            self.ip = value
        if name in ("-p", "--port"):
            self.port = value
        if name in ("-s", "--size"):
            self.size = value
