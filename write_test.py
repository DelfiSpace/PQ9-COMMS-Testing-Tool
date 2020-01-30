import ByteWriter
import collections
import NRZI_G3RUH_Encoder
import AX25_Encoder
import random
from BitLib import *

bwrite = ByteWriter.ByteWriter()
g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()
ax25Encoder = AX25_Encoder.AX25Encoder()

pilot_seq = (100*[int("0x7E", 16), int("0x7E", 16)])
tail_seq = 1*[int("0x7E", 16), int("0x7E", 16)]
data = [int("0x88", 16), int("0x98", 16),int("0x98", 16), int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0xE0", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x61", 16), int("0x03", 16), int("0xF0", 16)]
data += [2, 4, 99, 1, 1, 4, 0]#[random.randint(0,255) for i in range(0,15)]
data.extend(ax25Encoder.CalculateFCS(data))

data2 = [int("0x88", 16), int("0x98", 16),int("0x98", 16), int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0xE0", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x61", 16), int("0x03", 16), int("0xF0", 16)]
data2 += [2, 4, 99, 1, 1, 4, 1]#[random.randint(0,255) for i in range(0,15)]
data2.extend(ax25Encoder.CalculateFCS(data2))
 
txBits = list2bits(pilot_seq) + 1*((ax25Encoder.StuffBits(list2bits(flipbytes(data))) + list2bits(tail_seq)) + (ax25Encoder.StuffBits(list2bits(flipbytes(data2))) + list2bits(tail_seq))) + list2bits(pilot_seq)
txBits_raw = txBits
#txBits = [ax25encoder.NRZIEncodeBit(ax25encoder.ScrambleBit(x)) for x in txBits_raw]
txBits = [g3ruhEncoder.NRZIEncodeBit(g3ruhEncoder.ScrambleBit(x)) for x in txBits_raw]
txBytes = bits2bytes(txBits)

bwrite.writeBytes(txBytes)
