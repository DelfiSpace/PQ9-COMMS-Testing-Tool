import ByteWriter
import collections
import NRZI_G3RUH_Encoder
import random
import LDPC_generator_CCSDS_256 as LDPCCoder
import numpy as np
from BitLib import *

bwrite = ByteWriter.ByteWriter()
g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()

pilot_seq = (10*[int("0x7E", 16), int("0x7E", 16)])
start_seq = [int("0x00", 16), int("0x00", 16), int("0xEB", 16), int("0x90", 16),int("0x00", 16), int("0x00", 16), int("0xEB", 16), int("0x90", 16)]
tail_seq = [int("0xFF", 16), int("0xFF", 16), int("0xEB", 16), int("0x90", 16),int("0xFF", 16), int("0xFF", 16), int("0xEB", 16), int("0x90", 16)]
txBits = list2bits(pilot_seq) + list2bits(start_seq) 

for p in range(3):
    data = [random.randint(0,255) for i in range(0,32)]
    data = np.array(data, dtype=int)
    print("UNCODED DATA:")
    print(''.join('{:02X} '.format(x) for x in (data)))
    data = bits2bytes(np.mod(list2bits(data)@LDPCCoder.LDPC_getG(),2))
    print("CODED DATA:")
    print(''.join('{:02X} '.format(x) for x in (data)))
    txBits = txBits + list2bits(data)

txBits = txBits + list2bits(tail_seq)

txBits_raw = txBits
#txBits = [ax25encoder.NRZIEncodeBit(ax25encoder.ScrambleBit(x)) for x in txBits_raw]
txBits = [g3ruhEncoder.NRZIEncodeBit(g3ruhEncoder.ScrambleBit(x)) for x in txBits_raw]
txBytes = bits2bytes(txBits)

bwrite.writeBytes(txBytes)
