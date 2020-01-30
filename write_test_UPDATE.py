import ByteWriter
import collections
import NRZI_G3RUH_Encoder
import AX25_Encoder
import random
import time
from BitLib import *

bwrite = ByteWriter.ByteWriter()
g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()
ax25Encoder = AX25_Encoder.AX25Encoder()

pilot_seq = (200*[int("0x7E", 16), int("0x7E", 16)])
tail_seq = 50*[int("0x7E", 16), int("0x7E", 16)]
data_init = [int("0x88", 16), int("0x98", 16),int("0x98", 16), int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0xE0", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x61", 16), int("0x03", 16), int("0xF0", 16)]

txBits = list2bits(pilot_seq)

inputFilename = "Test.pq9"
fillup = False
fo = open(inputFilename, "r")
commandlines = fo.readlines()

for i, commandline in enumerate(commandlines):
    data =  (commandline.rstrip("\n")).split(" ")
    data = list(map(int, data))
    if fillup:
        command = data_init + [2, len(data), 99] + data
    else:
        command = data_init + data
    command.extend(ax25Encoder.CalculateFCS(command))
    txBits += (ax25Encoder.StuffBits(list2bits(flipbytes(command))) + list2bits(tail_seq))
    print(i)

txBits += list2bits(pilot_seq)
txBits_raw = txBits
#txBits = [ax25encoder.NRZIEncodeBit(ax25encoder.ScrambleBit(x)) for x in txBits_raw]
txBits = [g3ruhEncoder.NRZIEncodeBit(g3ruhEncoder.ScrambleBit(x)) for x in txBits_raw]
txBytes = bits2bytes(txBits)

bwrite.writeBytes(txBytes)
