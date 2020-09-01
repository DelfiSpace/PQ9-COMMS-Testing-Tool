import ByteWriter_continuous
import collections
import NRZI_G3RUH_Encoder
import AX25_Encoder
import random
import time
from multiprocessing import Process, Queue
from BitLib import *
import sys
import ByteReader
import AX25_Detector
from serial import Serial

def completeIdle(idleByte):
    idleBits = list2bits([idleByte])
    counter = 0
    doubleZero = 0
    for inBit in idleBits:
        if inBit == 1:
            doubleZero = 0
            counter = counter + 1
        if inBit == 0:
            if(counter == 0):
                doubleZero = 1
            counter = 0
    if(counter > 0):
        return (6-counter)*[1] + [0]
    if(doubleZero == 1):
        return 6*[1] + [0]
    
    return []

def byteSender(queue):
    writeQ = queue
    bwriter = ByteWriter_continuous.ByteWriter()
    idle_seq = 1*[int("0x7E", 16)]
    g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()
    while True:
        if(writeQ.empty()):
            txBits = [g3ruhEncoder.NRZIEncodeBit(g3ruhEncoder.ScrambleBit(x)) for x in list2bits(idle_seq)]
            txBytes = bits2bytes(txBits)
            #print("Buffering: ", end="")
            #print(''.join('{:02X} '.format(x) for x in txBytes))
            bwriter.writeBytes(txBytes)
            #print(idle_seq)
        else:
            #print("Qued up!!!!")
            txBytes = writeQ.get()
            txBits = list2bits(txBytes)
            # print("%02X"%idle_seq[0])
            # print(completeIdle(idle_seq[0]))
            txBits = completeIdle(idle_seq[0]) + txBits
            idle_seq = [(txBytes[-1])]
            txBytes = bits2bytes(txBits)
            txBits = [g3ruhEncoder.NRZIEncodeBit(g3ruhEncoder.ScrambleBit(x)) for x in list2bits(txBytes)]
            txBytes = bits2bytes(txBits)
            bwriter.writeBytes(txBytes)
            #print(self.writeQ.get())


def byteReceiver(queue):
    bread = ByteReader.ByteReader()
    g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()
    ax25Detector = AX25_Detector.AX25Detector()
    readQ = queue
    num = 0
    while True:
        #  Wait for next request from client
        rcvd, inbits = bread.GetBits()
        #print(''.join('{:02x} '.format(x) for x in message))
        #  Add received bytes to bitBuffer
        if(rcvd):
            for inbit_raw in inbits:
                inbit = g3ruhEncoder.DescrambleBit(g3ruhEncoder.NRZIDecodeBit(inbit_raw))
                rcflag, msg = ax25Detector.queBitwReturn(inbit)
                if(rcflag):
                    print("AX25 MSG RECEIVED! MSG: ", end="")
                    print(''.join('{:02X} '.format(x) for x in msg))
                    print("!RX: " + str(num) )
                    num+=1
                    readQ.put(msg)

def msgHandler(cmdQ, writeQ):
    #serPort = Serial('/dev/ttyACM0', timeout=10)
    #print("Connected to Serial: "+serPort.name)
    ax25Encoder = AX25_Encoder.AX25Encoder()
    data_init = [int("0x88", 16), int("0x98", 16),int("0x98", 16), int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0xE0", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x61", 16), int("0x03", 16), int("0xF0", 16)]
    ax25Encoder = AX25_Encoder.AX25Encoder()

    fillup = False
    while True:
        if(cmdQ.empty() == False):
            command = cmdQ.get()
            # #command = "2 4 99 1 1 4 1"
            # data =  (command.rstrip("\n")).split(" ")
            # data = list(map(int, data))
            # print("Command input: " + str(data))
            # command = data_init + data
            # command.extend(ax25Encoder.CalculateFCS(command))
            # txBits += (ax25Encoder.StuffBits(list2bits(flipbytes(command))) + list2bits(tail_seq))
            # writeQ.put(txBits)
            #bwrite = ByteWriter_continuous.ByteWriter()
            ax25Encoder = AX25_Encoder.AX25Encoder()

            pilot_seq = (4*[int("0x7E", 16)])
            tail_seq = 1*[int("0x7E", 16), int("0x7E", 16)]
            #data_init = [int("0x88", 16), int("0x98", 16),int("0x98", 16), int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0xE0", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x61", 16), int("0x03", 16), int("0xF0", 16)]

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
                    command = data_init + [i] + data
                command.extend(ax25Encoder.CalculateFCS(command))
                txBits += ax25Encoder.StuffBits(list2bits(flipbytes(command))) + list2bits(tail_seq)
                #print("Line number: " + str(i)+"  : ", end="")
                #print(''.join('{:02X} '.format(x) for x in command))
            #txBits += list2bits(pilot_seq)
            txBytes = bits2bytes(txBits+list2bits(tail_seq))
            #writeQ.put(txBytes)
            #print("Buffering: ", end="")
            #print(''.join('{:02X} '.format(x) for x in txBytes))
            writeQ.put(txBytes)
            #for byte in txBytes:
            #    writeQ.put([byte])
            # reply = False
            # START = time.time()
            # while reply == False:
            #     test = serPort.readline()
            #     if( test == b'!\r\n'):
            #         reply = True
            #     if(time.time()-START > 10):
            #         break
            # print(time.time()-START)


if __name__ == "__main__":
    writeQueue = Queue()
    readQueue = Queue()
    cmdQue = Queue()
    writer = Process(target=byteSender, daemon=True ,args=(writeQueue,))
    reader = Process(target=byteReceiver, daemon=True ,args=(readQueue,))
    msgHand = Process(target=msgHandler, daemon=True ,args=(cmdQue,writeQueue,))
    workers = [writer, reader, msgHand]
    for w in workers:
        w.daemon = True
        w.start()

    while True:
        txt = input()
        print("Transmit Test.pq9!")
        cmdQue.put(txt)

    for w in workers:
        w.join()
