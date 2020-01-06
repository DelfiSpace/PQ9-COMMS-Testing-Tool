

class AX25Encoder:

    def __init__(self):
        super().__init__()
        self.NRZI_ENCODER = True
        self.NRZI_DECODER = True
        self.scrambling_bit = 0
        self.scrambler = 255
        self.descrambling_bit = 0
        self.descrambler = 0

    def StuffBits(self, bits):
        outputBits = []
        counter = 0
        for bit in bits:
            if bit == 1:
                outputBits.append(1)
                counter = counter + 1
                if counter >= 5:
                    outputBits.append(0)
                    counter = 0
            else:
                outputBits.append(0)
                counter = 0

        return outputBits
        
    def DeStuffBits(self, bits):
        outputBits = []
        counter = 0
        for bit in bits:
            if bit == 1:
                outputBits.append(1)
                counter = counter + 1
            else:
                if counter < 5:
                    outputBits.append(0)
                counter = 0

        return outputBits

    def CalculateFCS(self, bytes):
        guard = False
        FCSBuff = int("0xFFFF",16)
        for byte in bytes:
            for i in range(0,8):
                guard = (FCSBuff & 1) != 0
                FCSBuff = FCSBuff >> 1
                FCSBuff = FCSBuff & int("0x7FFF", 16)
                bitHigh = (byte & (1 << i)) != 0
                if bitHigh != guard:
                    FCSBuff = FCSBuff ^ int("0x8408", 16)
        
        FCSBuff = FCSBuff ^ int("0xFFFF", 16)
        FCSByte1 = (FCSBuff & int("0x00FF",16))
        FCSByte2 = ((FCSBuff & int("0xFF00",16)) >> 8)

        return [FCSByte1, FCSByte2]

        