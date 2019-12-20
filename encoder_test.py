import ByteWriter
import collections
import NRZI_G3RUH_Encoder

def byte2bits(n):
    out = list([])
    out.extend(int(digit) for digit in format(n, "08b"))
    return out
def list2bits(p):
    out = list([])
    for n in p:
        out += list(byte2bits(n))
    return out
def bits2byte(n):
    out = 0
    for bit in n:
        out = (out << 1) | bit
    return out
def bits2bytes(n):
    out = []
    nr_of_bytes = int(len(n)/8)
    for i in range(0,nr_of_bytes):
        out.append(int(bits2byte(n[8*i:8*(i+1)])))
    return out

bwrite = ByteWriter.ByteWriter()
ax25encoder = NRZI_G3RUH_Encoder.AX25Encoder()

pilot_seq = 5*[int("0x7E", 16)]
start_seq = [int("0xEB", 16), int("0x90", 16), int("0x88", 16)]
tail_seq = [int("0x7E", 16), int("0x7E", 16)]
data = [int("0xCA", 16), int("0x59", 16), int("0xE4", 16)]

txBytes = pilot_seq + start_seq + data + tail_seq
print(txBytes)
txBits_raw = list2bits(txBytes)
#txBits = [ax25encoder.NRZIEncodeBit(ax25encoder.ScrambleBit(x)) for x in txBits_raw]
txBits = [ax25encoder.ScrambleBit(x) for x in txBits_raw]
txBytes = bits2bytes(txBits)
print(txBytes)

rxBits_raw = list2bits(txBytes)
rxBits = [ax25encoder.DescrambleBit(x) for x in rxBits_raw]
rxBytes = bits2bytes(rxBits)
print(rxBytes)