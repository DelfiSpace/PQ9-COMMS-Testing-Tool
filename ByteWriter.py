import time
import zmq
import collections
import numpy as np
from BitLib import *

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
