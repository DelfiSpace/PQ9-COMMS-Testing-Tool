import time
import zmq
import collections
import numpy as np
from BitLib import *

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
