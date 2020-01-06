import collections
import ByteReader
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

flagbuffer = collections.deque(maxlen = 24)
messagebuffer = (18+10)*8*[0]
bitcount = 0
rx_state = 0
#0 : Waiting for Flag;
#1 : receiving, waiting for flag or >max_size
bread = ByteReader.ByteReader()
g3ruhEncoder = NRZI_G3RUH_Encoder.AX25Encoder()
ax25Encoder = AX25_Encoder.AX25Encoder()

while True:
    #  Wait for next request from client
    rcvd, inbits = bread.GetBits()
    #print(''.join('{:02x} '.format(x) for x in message))
    #  Add received bytes to bitBuffer
    if(rcvd):
        for inbit_raw in inbits:
            inbit = g3ruhEncoder.DescrambleBit(g3ruhEncoder.NRZIDecodeBit(inbit_raw))
            if rx_state == 0:
                flagbuffer.append(inbit)
                if(bits2byte(list(flagbuffer)[0:8]) == int("0x7E", 16) and bits2byte(list(flagbuffer)[8:16]) == int("0x7E", 16) and bits2byte(list(flagbuffer)[16:24]) != int("0x7E", 16)):
                    rx_state = 1
                    #print("AX25 FLAG DETECTED  |  FirstByte", end="")
                    #print(''.join('{:02X} '.format(bits2byte(list(flagbuffer)[16:24]))))
                    messagebuffer = list(flagbuffer)[16:24]
                    bitcount = 8
            elif rx_state == 1:
                messagebuffer.append(inbit)
                bitcount += 1
                if(bitcount >= 8):
                    if(bits2byte(list(messagebuffer[bitcount-8:bitcount-1])) == int("0x7E", 16)):
                        messagebuffer = messagebuffer[:len(messagebuffer)-8]
                        messagebuffer = ax25Encoder.DeStuffBits(messagebuffer)
                        if (len(messagebuffer)-1) % 8 == 0:
                            print("END SEQ, LEN: %2d | MSG: " % int((len(messagebuffer)-1)/8), end="")
                            print(''.join('{:02X} '.format(flipbyte(x)) for x in bits2bytes(messagebuffer[:bitcount-9])))
                        bitcount = 0
                        rx_state = 0
                if(bitcount >= (18+10)*8):
                    bitcount = 0
                    rx_state = 0
            #print(bitbuffer)