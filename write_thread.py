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

def byteSender(queue):
    writeQ = queue
    bwriter = ByteWriter_continuous.ByteWriter()
    idle_seq = [int("0x7E", 16)]
    g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()
    while True:
        if(writeQ.empty()):
            txBits = [g3ruhEncoder.NRZIEncodeBit(g3ruhEncoder.ScrambleBit(x)) for x in list2bits(idle_seq)]
            txBytes = bits2bytes(txBits)
            bwriter.writeBytes(txBytes)
            #print(idle_seq)
        else:
            #print("Qued up!!!!")
            txByte = writeQ.get()
            txBits = [g3ruhEncoder.NRZIEncodeBit(g3ruhEncoder.ScrambleBit(x)) for x in list2bits(txByte)]
            txBytes = bits2bytes(txBits)
            bwriter.writeBytes(txBytes)
            #print(self.writeQ.get())


def byteReceiver(queue):
    bread = ByteReader.ByteReader()
    g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()
    ax25Encoder = AX25_Encoder.AX25Encoder()
    ax25Detector = AX25_Detector.AX25Detector()
    readQ = queue
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
                    readQ.put(msg)

def msgHandler(cmdQ, writeQ):
    ax25Encoder = AX25_Encoder.AX25Encoder()
    pilot_seq = (200*[int("0x7E", 16), int("0x7E", 16)])
    tail_seq = 1*[int("0x7E", 16), int("0x7E", 16)]
    data_init = [int("0x88", 16), int("0x98", 16),int("0x98", 16), int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0xE0", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x40", 16),int("0x61", 16), int("0x03", 16), int("0xF0", 16)]
    g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()
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
            g3ruhEncoder = NRZI_G3RUH_Encoder.G3RUHEncoder()
            ax25Encoder = AX25_Encoder.AX25Encoder()

            pilot_seq = (200*[int("0x7E", 16), int("0x7E", 16)])
            tail_seq = 10*[int("0x7E", 16), int("0x7E", 16)]
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
                txBits += (ax25Encoder.StuffBits(list2bits(flipbytes(command))) + list2bits(2*tail_seq))
                print("Line number: " + str(i))

            txBits += list2bits(pilot_seq)
            txBits_raw = txBits
            #txBits = [ax25encoder.NRZIEncodeBit(ax25encoder.ScrambleBit(x)) for x in txBits_raw]
            txBytes = bits2bytes(txBits)
            txBytes =  50*[int("0xAA", 16)] + txBytes + 50*[int("0xAA", 16)]
            #writeQ.put(txBytes)
            for byte in txBytes:
                writeQ.put([byte])


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
        cmdQue.put(txt)

    for w in workers:
        w.join()
