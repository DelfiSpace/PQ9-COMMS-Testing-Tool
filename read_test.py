import collections
import ByteReader

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

while True:
    #  Wait for next request from client
    rcvd, inbits = bread.GetBits()
    #print(''.join('{:02x} '.format(x) for x in message))
    #  Add received bytes to bitBuffer
    if(rcvd):
        for inbit in inbits:
            if rx_state == 0:
                flagbuffer.append(inbit)
                if(bits2byte(list(flagbuffer)[0:8]) == int("0xEB", 16) and bits2byte(list(flagbuffer)[8:16]) == int("0x90", 16) and bits2byte(list(flagbuffer)[16:24]) == int("0x88", 16)):
                    rx_state = 1
                    print("AX25 FLAG DETECTED")
            elif rx_state == 1:
                messagebuffer[bitcount] = inbit
                bitcount += 1
                if(bitcount >= 8):
                    if(bits2byte(list(messagebuffer[bitcount-8:bitcount-1])) == int("0x7E", 16)):
                        print("END SEQ, LEN: %2d | MSG: " % int((bitcount-8)/8), end="")
                        print(''.join('{:02X} '.format(x) for x in bits2bytes(messagebuffer[:bitcount-9])))
                        bitcount = 0
                        rx_state = 0
                if(bitcount >= (18+10)*8):
                    bitcount = 0
                    rx_state = 0
            #print(bitbuffer)