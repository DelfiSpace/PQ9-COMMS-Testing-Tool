import NRZI_G3RUH_Encoder
import AX25_Encoder
import AX25_Detector_FEC
import random
import numpy as np
from BitLib import *

g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()
ax25Encoder = AX25_Encoder.AX25Encoder()
ax25Detector = AX25_Detector_FEC.AX25Detector()

for i in range(0,1):
    ##  SENDER
    pilot_seq = (50*[int("0x7E", 16)])
    tail_seq = (20*[int("0x7E", 16)])
    data = [int("0x82", 16), int("0x98", 16),int("0x98", 16), int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0xE0", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x61", 16), int("0x03", 16), int("0xF0", 16)]
    data += [random.randint(0,255) for i in range(0,35)]
    data.extend(ax25Encoder.CalculateFCS(data))
    txBits = list2bits(pilot_seq) + 1*(ax25Encoder.StuffBits(list2bits(flipbytes(data))) + list2bits(tail_seq)) + list2bits(pilot_seq)
    #print("TX MSG: ")
    #print(''.join('{:02X} '.format(x) for x in data))
    txBits_raw = txBits
    txBits = [g3ruhEncoder.NRZIEncodeBit(g3ruhEncoder.ScrambleBit(x)) for x in txBits_raw]


    ## CHANNEL 16 8 6 4 2
    EbN = 25 #dB
    channelBits = np.array(txBits)
    SNR_lin = 10**(EbN/10)
    No = 1.0/SNR_lin
    sigma = np.sqrt(No/2)

    channelBits = 2*channelBits - 1 
    channelBits = channelBits + sigma*np.random.randn(channelBits.size)

    ## RECEIVER
    Lc = 2/(sigma**2)
    rxBits = Lc * channelBits
    for rxBit in rxBits:
        ax25Detector.queBit_FEC_FIXED_LEN(rxBit,53)


