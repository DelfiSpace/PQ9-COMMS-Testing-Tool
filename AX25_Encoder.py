

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