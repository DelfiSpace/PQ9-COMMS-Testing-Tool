import collections
import AX25_Encoder
import LDPC_decoder
import LDPC_generator_CCSDS_256
from BitLib import *

class APDetector:

    def __init__(self):
        super().__init__()
        self.state = 0
        self.state = 0
        self.flagbuffer = collections.deque(24*[0],maxlen = 24)
        self.msgBuffer = []
        self.bitCount = 0
        self.LDPCdecoder = LDPC_decoder.decoder(LDPC_generator_CCSDS_256.H)

    def queBit(self, bit):
        if self.state == 0:
            ##Detect Flag
            self.flagbuffer.append(bit)
            if compareBytes(bits2bytes(list(self.flagbuffer)), [int("0x7E", 16), int("0xEB", 16), int("0x90", 16)]) <= 1:
                print("FLAG DETECTED")
                self.msgBuffer = []
                self.state = 2
        elif self.state == 2:
            ##receiving message pilot
            self.msgBuffer.append(bit)
            self.bitCount = self.bitCount + 1
            #print(self.bitCount)
            if self.bitCount >= 8*64:
                ## pilot received!
                decoded = False
                ##decode pilot:
                for k in range(0,20):
                    #print("DECODING!")
                    decoded, self.msgBuffer = self.LDPCdecoder.iterateBitFlip(self.msgBuffer)
                    if decoded:
                        break
                if decoded:
                    receivedBytes = (bits2bytes(self.msgBuffer))[:32]
                    print("AP MSG RECEIVED! | ITER: %2d | LEN: %2d | MSG: " % (k, int(len(receivedBytes))), end="")
                    print(''.join('{:02X} '.format(x) for x in receivedBytes))
                else:
                    print("PILOT FAILED TO DECODE")
                self.msgBuffer = []
                self.bitCount = 0
                self.state = 0