#program to convert raw IQ file to csv to test in Paraview
# Written by Stephen Hamilton 
# 31 Dec 2019


import sys
import struct
import math
import pdb


def main():
    #Check to see if a filename was given
    if (len(sys.argv) < 2):
        print("Please specify a file name to read.")
        exit(1)
    
    infile = sys.argv[1]
    print("Processing file ", infile)
    try:
        iqdata = open(infile, "rb")
    except Exception as e:
        print("Unable to open ", infile)
        print ("Exception is: ", e)

    #setup output file
    outfile = open("out.csv", "w")
    outfile.write('i, q, t, c\n') # inphase, quadrature, time, and color (angle of i and q?)

    buf_size=1024*64 
    x = 0
    y = 0 
    t = 0
    while True:
        data=iqdata.read(buf_size)
        if not data: break
        if (len(data) < buf_size):
            print("Almost done.")
        data_range = len(data)
        for c in range (0, data_range, 8):
            i = struct.unpack('f', data[c:c+4])
            q = struct.unpack('f', data[c+4:c+8])
            #print ("I is %f and Q is %f" % (i[0], q[0]))
            #write the points
            if (q[0] == 0):
                color = 0
            else:
                color = math.tan(i[0]/q[0])
            outfile.write(str((i[0])*1000.0) + ', ')
            outfile.write(str((q[0])*1000.0) + ', ' + str(float(t/100)) + ', ' +str(color) + '\n')
            x= x +1
            t = t + 1
        y= y +1 
        x = 0          

    outfile.close()    
    iqdata.close()

if __name__ == '__main__':
    main()
