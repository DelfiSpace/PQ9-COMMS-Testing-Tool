import time
import zmq
import collections
import numpy as np

def byte2bits(n):
    out = list([])
    out.extend(int(digit) for digit in format(n, "08b"))
    return out
def list2bits(p):
    out = list([])
    for n in p:
        out += list(byte2bits(n))
    return out
def bits2byte(n):
    out = 0
    for bit in n:
        out = (out << 1) | bit
    return out
def bits2bytes(n):
    out = []
    nr_of_bytes = int(len(n)/8)
    for i in range(0,nr_of_bytes):
        out.append(int(bits2byte(n[8*i:8*(i+1)])))
    return out

class ByteReader:

    def __init__(self):
        super().__init__()
        #  Socket to talk to server
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        print("Connecting to port 5500")
        self.socket.connect("tcp://127.0.0.1:5500")

    def GetBits(self):
        try:
            #  Wait for next request from client
            message = self.socket.recv(flags = zmq.NOBLOCK)
            #print(''.join('{:02x} '.format(x) for x in message))
            #  Add received bytes to bitBuffer
            inbits = list2bits(list(message))
            return True, inbits
        except zmq.Again as e:
            return False, []
