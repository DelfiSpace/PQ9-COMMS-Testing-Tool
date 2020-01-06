import ByteWriter
import collections
import NRZI_G3RUH_Encoder
import AX25_Encoder

def flipbyte(x):
    return int((format(x,"08b")[::-1]),2)

def flipbytes(n):
    out = list([])
    out.extend(int((format(x,"08b")[::-1]),2) for x in n)
    return out

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
g3ruhEncoder = NRZI_G3RUH_Encoder.AX25Encoder()
ax25Encoder = AX25_Encoder.AX25Encoder()

pilot_seq = list2bits(3*[int("0x7E", 16), int("0x7E", 16)])
tail_seq = list2bits([int("0x7E", 16), int("0x7E", 16)])
data = list2bits(flipbytes([int("0x82", 16), int("0x98", 16),int("0x98", 16), int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0xE0", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x61", 16), int("0x03", 16), int("0xF0", 16), int("0xFF", 16),int("0xFF", 16),int("0x54", 16),int("0x05", 16)]))

txBits = pilot_seq + ax25Encoder.StuffBits(data) + tail_seq

txBits_raw = txBits
#txBits = [ax25encoder.NRZIEncodeBit(ax25encoder.ScrambleBit(x)) for x in txBits_raw]
txBits = [g3ruhEncoder.NRZIEncodeBit(g3ruhEncoder.ScrambleBit(x)) for x in txBits_raw]
txBytes = bits2bytes(txBits)

bwrite.writeBytes(txBytes)
