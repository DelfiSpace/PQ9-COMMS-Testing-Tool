import collections
import AX25_Encoder
from BitLib import *

class AX25Detector:

    def __init__(self):
        super().__init__()
        self.state = 0
        self.state = 0
        self.flagbuffer = collections.deque(maxlen = 8)
        self.msgBuffer = []
        self.bitCount = 0

    def queBit(self, bit):
        if self.state == 0:
            ##Detect Flag
            self.flagbuffer.append(bit)
            if bits2byte(list(self.flagbuffer)) == int("0x7E", 16):
                #print("FLAG DETECTED")
                self.msgBuffer = []
                self.state = 1
        elif self.state == 1:
            ##Check for message start
            self.msgBuffer.append(bit)
            self.bitCount = self.bitCount + 1
            if (self.bitCount == 8):
                if bits2byte(list(self.msgBuffer)) == int("0x7E", 16):
                    ##first incoming byte is another flag, so drop this byte
                    #print("Another flag!")
                    self.msgBuffer = []
                    self.bitCount = 0
                else:
                    ##first incoming byte was not a flag, so the message has started!
                    #print("MESSAGE START!")
                    self.state = 2
        elif self.state == 2:
            ##receiving message
            self.msgBuffer.append(bit)
            self.bitCount = self.bitCount + 1
            if bits2byte(list(self.msgBuffer[-8:])) == int("0x7E", 16):
                ##end sequence detected!

                ##destuff msg:
                self.msgBuffer = AX25_Encoder.AX25Encoder.DeStuffBits(self.msgBuffer[:-8])
                if len(self.msgBuffer)%8 == 0 and len(self.msgBuffer) > 18*8:
                    receivedBytes = flipbytes(bits2bytes(self.msgBuffer))
                    if (AX25_Encoder.AX25Encoder.CheckFCS(receivedBytes)):
                        print("AX25 MSG RECEIVED! | LEN: %2d | MSG: " % int(len(receivedBytes)), end="")
                        print(''.join('{:02X} '.format(x) for x in receivedBytes))
                self.msgBuffer = []
                self.bitCount = 0
                self.state = 0
            if self.bitCount >= (512+18)*8:
                ##msg too long, hence not a msg
                #print("MSG too long!")
                self.msgBuffer = []
                self.bitCount = 0
                self.state = 0