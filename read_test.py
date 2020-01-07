import collections
import ByteReader
import NRZI_G3RUH_Encoder
import AX25_Encoder
from BitLib import *
import AX25_Detector
import AP_Detector

flagbuffer = collections.deque(maxlen = 16)
bitcount = 0
rx_state = 0
#0 : Waiting for Flag;
#1 : receiving, waiting for flag or >max_size
bread = ByteReader.ByteReader()
g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()
ax25Encoder = AX25_Encoder.AX25Encoder()
ax25Detector = AX25_Detector.AX25Detector()
apDetector = AP_Detector.APDetector()

while True:
    #  Wait for next request from client
    rcvd, inbits = bread.GetBits()
    #print(''.join('{:02x} '.format(x) for x in message))
    #  Add received bytes to bitBuffer
    if(rcvd):
        for inbit_raw in inbits:
            inbit = g3ruhEncoder.DescrambleBit(g3ruhEncoder.NRZIDecodeBit(inbit_raw))
            ax25Detector.queBit(inbit)
            apDetector.queBit(inbit)