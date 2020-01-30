import ByteWriter
import time
from BitLib import *
import collections
import ByteReader
import NRZI_G3RUH_Encoder
import AX25_Encoder
import AX25_Detector


bread = ByteReader.ByteReader()
g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()
ax25Encoder = AX25_Encoder.AX25Encoder()
ax25Detector = AX25_Detector.AX25Detector()

bwrite = ByteWriter.ByteWriter()
g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()
ax25Encoder = AX25_Encoder.AX25Encoder()

pilot_seq = (17*[int("0x7E", 16), int("0x7E", 16)])
tail_seq = 1*[int("0x7E", 16), int("0x7E", 16)]
data_init = [int("0x88", 16), int("0x98", 16),int("0x98", 16), int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0xE0", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x61", 16), int("0x03", 16), int("0xF0", 16)]

txBits = list2bits(pilot_seq)

inputFilename = "Test.pq9"
fillup = True
fo = open(inputFilename, "r")
commandlines = fo.readlines()

for i, commandline in enumerate(commandlines):
    cmdSucces = False
    while(cmdSucces == False):
        #time.sleep(0.5)
        startTime = time.time()
        replyReceived = False
        data =  (commandline.rstrip("\n")).split(" ")
        data = list(map(int, data))
        if fillup:
            command = data_init + [2, len(data), 99] + data
        else:
            command = data_init + data
        command.extend(ax25Encoder.CalculateFCS(command))
        txBits += (ax25Encoder.StuffBits(list2bits(flipbytes(command))) + list2bits(tail_seq))
        print("Line number: " + str(i))
        txBits_raw = txBits
        #txBits = [ax25encoder.NRZIEncodeBit(ax25encoder.ScrambleBit(x)) for x in txBits_raw]
        txBits = [g3ruhEncoder.NRZIEncodeBit(g3ruhEncoder.ScrambleBit(x)) for x in txBits_raw]
        txBytes = bits2bytes(txBits)
        bwrite.writeBytes(txBytes)

        replyReceived = False
        while(replyReceived==False):
            rcvd, inbits = bread.GetBits()
            if(rcvd):
                for inbit_raw in inbits:
                    inbit = g3ruhEncoder.DescrambleBit(g3ruhEncoder.NRZIDecodeBit(inbit_raw))
                    replied = ax25Detector.queBit(inbit)
                    if(replied):
                        replyReceived = True
                        cmdSucces = True
                        break
            if(time.time() - startTime > 2): #timeout
                print("no reply.")
                replyReceived = True
        #wait for reply!
        txBits = list2bits(pilot_seq)