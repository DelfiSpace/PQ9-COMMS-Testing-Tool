import collections
import AX25_Encoder
import NRZI_G3RUH_Encoder
import numpy as np
from BitLib import *

class AX25Detector:

    def __init__(self):
        super().__init__()
        self.state = 0
        self.state = 0
        self.flagbuffer = collections.deque(maxlen = 8)
        self.msgBuffer = []
        self.msgBuffer_raw = []
        self.bitCount = 0
        self.packetCount = 0
        self.g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()

    def queBit_FEC(self, y):
        if self.state == 0:
            ##Detect Flag
            inbit = soft2hardBit(y)
            bit = self.g3ruhEncoder.DescrambleBit(self.g3ruhEncoder.NRZIDecodeBit(inbit))

            self.flagbuffer.append(bit)
            if compareByte(bits2byte(list(self.flagbuffer)), int("0x7E", 16)) <= 1:
                #print("FLAG DETECTED")
                self.msgBuffer = []
                self.msgBuffer_raw = []
                self.state = 1
                self.g3ruhEncoder.SaveState()
        elif self.state == 1:
            inbit = soft2hardBit(y)
            bit = self.g3ruhEncoder.DescrambleBit(self.g3ruhEncoder.NRZIDecodeBit(inbit))
            ##Check for message start
            self.msgBuffer_raw.append(y)
            self.msgBuffer.append(bit)
            self.bitCount = self.bitCount + 1
            if (self.bitCount == 8):
                if compareByte(bits2byte(list(self.msgBuffer)), int("0x7E", 16)) <= 1:
                    ##first incoming byte is another flag, so drop this byte
                    #print("Another flag!")
                    self.msgBuffer = []
                    self.msgBuffer_raw = []
                    self.bitCount = 0
                    self.g3ruhEncoder.SaveState()
                else:
                    ##first incoming byte was not a flag, so the message has started!
                    #print("MESSAGE START!")
                    self.state = 2
        elif self.state == 2:
            inbit = soft2hardBit(y)
            bit = self.g3ruhEncoder.DescrambleBit(self.g3ruhEncoder.NRZIDecodeBit(inbit))
            self.msgBuffer_raw.append(y)
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
                        self.packetCount += 1
                        print("AX25 MSG RECEIVED! | NR: %2d | LEN: %2d | MSG: " % (self.packetCount, int(len(receivedBytes))), end="")
                        print(''.join('{:02X} '.format(x) for x in receivedBytes))
                    else:
                        print("AX25 MSG FCS FAILED!  ", end = "")
                        self.iterateBitFlip(self.msgBuffer_raw[:-8])
                self.msgBuffer = []
                self.bitCount = 0
                self.state = 0
            if self.bitCount >= (512+18)*8:
                ##msg too long, hence not a msg
                #print("MSG too long!")
                self.msgBuffer = []
                self.bitCount = 0
                self.state = 0

    def iterateBitFlip(self, msg):
        n_bits = 5
        msg = np.array(msg)
        idx_unreliable = np.argsort(np.abs(msg))[:n_bits]
        print("Worst bits index: ", end = "")
        print(idx_unreliable, end = "")

        for i in range(1,2**n_bits + 1):
            ##brute force attack of worst N bits
            test1 = np.array([int(n) for n in format(i, "0%db" % (n_bits))])
            idx_slice = idx_unreliable[np.argwhere(test1 == 1)]
            msg_try_raw = np.copy(msg)
            msg_try_raw[idx_slice] *= -1
            #print(idx_slice)

            msg_try = []
            self.g3ruhEncoder.LoadState()
            for y in msg_try_raw:
                inbit = soft2hardBit(y)
                bit = self.g3ruhEncoder.DescrambleBit(self.g3ruhEncoder.NRZIDecodeBit(inbit))
                msg_try.append(bit)

            msg_try = AX25_Encoder.AX25Encoder.DeStuffBits(msg_try)
            receivedBytes = flipbytes(bits2bytes(msg_try))
            if (AX25_Encoder.AX25Encoder.CheckFCS(receivedBytes)):
                print(" - SUCCES ON FIX: "+ format(i, "0%db" % (n_bits)))
                self.packetCount += 1
                print("AX25 MSG FIXED   ! | NR: %2d | LEN: %2d | MSG: " % (self.packetCount, int(len(receivedBytes))), end="")
                print(''.join('{:02X} '.format(x) for x in receivedBytes))
                return
        print("AX25 MSG BROKEN")