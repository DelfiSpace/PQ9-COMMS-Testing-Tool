import ByteWriter
import collections
import NRZI_G3RUH_Encoder
import AX25_Encoder
import LDPC_generator_CCSDS_256 as LDPC
import LDPC_decoder as LDPCdecoder
import numpy as np
from BitLib import *

bwrite = ByteWriter.ByteWriter()
g3ruhEncoder = NRZI_G3RUH_Encoder.AX25Encoder()
ax25Encoder = AX25_Encoder.AX25Encoder()
pilot_seq = (3*[int("0x7E", 16), int("0x7E", 16)])
tail_seq = [int("0x7E", 16), int("0x7E", 16)]

PacketData = []
ACQ_SEQ = 2*[int("0xAA",16)]
START_SEQ = [int("0xEB",16), int("0x90",16)]
PacketData.extend(ACQ_SEQ)
PacketData.extend(START_SEQ)

nr_of_CLTU = 60
# # Create Pilot CLTU With Data:
PilotCLTU = [nr_of_CLTU, int("0x00",16)] + 30*[int("0xFF",16)]
u = np.array(list2bits(PilotCLTU), dtype=int)
print("UNCODED DATA: ")
print(''.join('{:02X} '.format(x) for x in bits2bytes(u)))
x = np.mod(u@LDPC.LDPC_getG(),2)
print("CODED DATA: ")
print(''.join('{:02x} '.format(u) for u in bits2bytes(x)))
PacketData.extend(bits2bytes(x))

for q in range(0,nr_of_CLTU):
    CLTU = np.random.randint(0,255,32).tolist()
    #CLTU = 16*[int("0xCA",16), int("0xBB",16)]
    x = np.mod(np.array(list2bits(CLTU), dtype=int)@LDPC.LDPC_getG(),2)
    PacketData.extend(bits2bytes(x))


PacketData.extend(ax25Encoder.CalculateFCS(PacketData))
txBits = list2bits(pilot_seq) + ax25Encoder.StuffBits(list2bits(flipbytes(PacketData))) + list2bits(tail_seq)

txBits_raw = txBits
#txBits = [ax25encoder.NRZIEncodeBit(ax25encoder.ScrambleBit(x)) for x in txBits_raw]
txBits = [g3ruhEncoder.NRZIEncodeBit(g3ruhEncoder.ScrambleBit(x)) for x in txBits_raw]
txBytes = bits2bytes(txBits)

bwrite.writeBytes(txBytes)