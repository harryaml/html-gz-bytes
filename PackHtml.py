#!/usr/bin/env python3

# very basic program to convert HTML file to HEX text representing the contents of the Gzipped HTML

print()
print("====PackHtml.py=====")
print()

#=================

import fileinput
import struct

from sh import gzip # sh needed to be installed with pip3

#=================
    # file names are hard-wired - too lazy to make a better user interface
inputFileName =  "indexTrain.html"
gzFileName =     "indexTrain.html.gz"
outputFileName = "indexTrain.h"

#=================
    # first compress the file
    # keep the input file, force overwrite of existing out file, put Name of file inside the GZ
gzip("-k", "-f", "-N", inputFileName)

#=================
    # now convert the bytes in the GZIP to hex text
gzFile = open(gzFileName, 'rb')
outFile = open(outputFileName, 'w')

hexCount = 0
byteCount = 0

    # first write header lines for the .h file as required by the C++ code that will use it
outFile.write("#define index_ov2640_html_gz_len NNNN\nconst uint8_t index_ov2640_html_gz[] = {\n")

    # deal with each byte
while True:
        # go through the compressed file byte by byte
    gzData = gzFile.read(1)
    if  len(gzData) == 0:
        break
    else:
            # unpack the byte
        unpacked = struct.unpack('>B', gzData)
        hexStr = "0x%0.2X, " % unpacked
        # ~ print ("%s  %s" %(unpacked, hexStr))
        outFile.write(hexStr)
        hexCount += 1
        byteCount += 1
        if hexCount >= 16:
            outFile.write("\n")
            hexCount = 0
            
    # write a closing }; to finish off the C++ code
outFile.write("\n};")
outFile.close()

#=================
    # open the .h file in a text editor and replace the NNNN with the following number
print(" === Done  %s bytes ===" %(byteCount))
