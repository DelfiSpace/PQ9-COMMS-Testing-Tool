from BitLib import *

class G3RUHEncoder:

    def __init__(self):
        super().__init__()
        self.NRZI_ENCODER = True
        self.NRZI_DECODER = True
        self.scrambling_bit = 0
        self.scrambler = 255
        self.descrambling_bit = 0
        self.descrambler = 0

    def ScrambleBit(self, bit):
        self.scrambling_bit = ((self.scrambler >> 11) & 1) ^ ((self.scrambler >> 16) & 1) ^ (bit & 1)
        self.scrambler <<= 1
        self.scrambler |= self.scrambling_bit & 1
        self.scrambler &= int("0x01FFFF",16)
        return self.scrambling_bit

    def DescrambleBit(self, bit):
        self.descrambling_bit = ((self.descrambler >> 11) & 1) ^ ((self.descrambler >> 16) & 1) ^ (bit & 1)
        self.descrambler <<= 1
        self.descrambler |= bit & 1
        self.descrambler &= int("0x01FFFF",16)
        return self.descrambling_bit

    def NRZIEncodeBit(self, inbit):
        isHigh = True if inbit > 0 else False
        self.NRZI_ENCODER = (self.NRZI_ENCODER != (not isHigh))
        return 1 if self.NRZI_ENCODER == True else 0

    def NRZIDecodeBit(self, inbit):
        isHigh = True if inbit > 0 else False
        tmp = self.NRZI_DECODER
        self.NRZI_DECODER = isHigh
        return 0 if (isHigh != tmp) else 1

    def SaveState(self):
        self.NRZI_ENCODER_bak = self.NRZI_ENCODER
        self.NRZI_DECODER_bak = self.NRZI_DECODER
        self.scrambling_bit_bak = self.scrambling_bit
        self.scrambler_bak = self.scrambler
        self.descrambling_bit_bak = self.descrambling_bit
        self.descrambler_bak = self.descrambler

    def LoadState(self):
        self.NRZI_ENCODER = self.NRZI_ENCODER_bak
        self.NRZI_DECODER = self.NRZI_DECODER_bak
        self.scrambling_bit = self.scrambling_bit_bak
        self.scrambler = self.scrambler_bak
        self.descrambling_bit = self.descrambling_bit_bak
        self.descrambler = self.descrambler_bak