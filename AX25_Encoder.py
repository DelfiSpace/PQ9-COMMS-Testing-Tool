

class AX25Encoder:

    @staticmethod
    def StuffBits(bits):
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
        
    @staticmethod
    def DeStuffBits(bits):
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

    @staticmethod
    def CalculateFCS(bytes):
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

    @staticmethod
    def CheckFCS(bytes):
        guard = False
        FCSBuff = int("0xFFFF",16)
        for k in range(0,len(bytes)-2):
            for i in range(0,8):
                guard = (FCSBuff & 1) != 0
                FCSBuff = FCSBuff >> 1
                FCSBuff = FCSBuff & int("0x7FFF", 16)
                bitHigh = (bytes[k] & (1 << i)) != 0
                if bitHigh != guard:
                    FCSBuff = FCSBuff ^ int("0x8408", 16)
        
        FCSBuff = FCSBuff ^ int("0xFFFF", 16)
        FCSByte1 = (FCSBuff & int("0x00FF",16))
        FCSByte2 = ((FCSBuff & int("0xFF00",16)) >> 8)

        return (FCSByte1 == bytes[-2] and FCSByte2 == bytes[-1])