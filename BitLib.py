## Collection of Bit-conversion helper functions
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

def compareByte(a, b):
    return sum(byte2bits(a^b))

def compareBytes(a, b):
    count = 0
    for i in range(0,len(a)):
        count = count + compareByte(a[i],b[i])
    return count