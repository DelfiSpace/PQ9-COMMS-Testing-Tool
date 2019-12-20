import ByteWriter
import collections

bwrite = ByteWriter.ByteWriter()

start_seq = [int("0xEB", 16), int("0x90", 16), int("0x88", 16)]
tail_seq = [int("0x7E", 16), int("0x7E", 16)]

data = [int("0xCA", 16), int("0x59", 16), int("0xE4", 16)]
bwrite.writeBytes( start_seq + data + tail_seq )
