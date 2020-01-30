import time
import zmq
import collections
import numpy as np
import NRZI_G3RUH_Encoder
from BitLib import *

class ByteWriter:

    def __init__(self):
        super().__init__()
        #  Socket to talk to server
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        print("ByteWriter: Binding to port 5600")
        self.socket.bind("tcp://*:5600")

    def writeBytes(self, intList):
        message = self.socket.recv()
        packet = intList
        MSG = []
        for x in range(0,len(packet)):
            MSG.extend(packet[x].to_bytes(1, 'big'))
        self.socket.send(bytes(MSG))
        #print(self.socket.get_hwm())