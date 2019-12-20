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
    for inbit in n:
        out = (out << 1) | inbit
    return out
def bits2bytes(n):
    out = []
    nr_of_bytes = int(len(n)/8)
    for i in range(0,nr_of_bytes):
        out.append(int(bits2byte(n[8*i:8*(i+1)])))
    return out

class ByteWriter:

    def __init__(self):
        super().__init__()
        #  Socket to talk to server
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        print("ByteWriter: Binding to port 5600")
        self.socket.bind("tcp://*:5600")

    def writeBytes(self, intList):
        packet = 50*[int("0xAA", 16)]
        # for i in range(0,171):
        #     #  Wait for next request from client
        #     packet += [int("0xEB", 16), int("0x90", 16), int("0x88", 16), i, int("0x0A", 16), int("0x03", 16), int("0x05", 16), int("0x06", 16), int("0x7E", 16), int("0x7E", 16)]
        packet += intList
        packet += 50*[int("0xAA", 16)]
        MSG = []
        for x in range(0,len(packet)):
            MSG.extend(packet[x].to_bytes(1, 'big'))
        self.socket.send(bytes(MSG))
