#program to convert raw IQ file to VTK Polydata.
# Written by Stephen Hamilton 
# 2 Jan 2020


import sys
import struct
import math
import pdb
import vtk
import numpy as np
from vtk.util import numpy_support

def get_files():
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
    outfilename = infile.split(".")
    outfile = open(outfilename[0], "w")
    #outfile.write('i, q, t, c\n') # inphase, quadrature, time, and color (angle of i and q?)
    return iqdata, outfile

def build_vtkfile(iqdata, outfile):
    rawiq = np.fromfile(iqdata, dtype='f', count = -1)
    point_count = int(rawiq.size/2)
    iqtwo = rawiq.reshape(point_count, 2)
    iqtwo = iqtwo*100 #scale the IQ data
    #z = np.arange(point_count)
    z = np.arange(0,10000,10000/point_count)  
    iqthree = np.column_stack((iqtwo,z))
    print(str(rawiq[0]), str(rawiq[1])) #sanity check
    vtkdata = numpy_support.numpy_to_vtk(iqthree, deep=True, array_type=vtk.VTK_FLOAT)
    vtkdata.SetNumberOfComponents(3)
    vtkdata.SetName("Points")
    #table = vtk.vtkTable
    #table.addColumn(vtkdata)
    points = vtk.vtkPoints()
    points.SetData(vtkdata)
    pd = vtk.vtkPolyData()
    pd.SetPoints(points)
    vv = vtk.vtkPointDataToCellData()
    vv.SetInputData(pd)
    vv.Update()
    
    
    w = vtk.vtkXMLPolyDataWriter()
    w.SetInputData(vv.GetOutput())
    w.SetFileName("autotest.vtp")
    w.Write()
    pdb.set_trace()


def main():
    iqdata, outfile = get_files()
    build_vtkfile(iqdata, outfile)
    outfile.close()    
    iqdata.close()

if __name__ == '__main__':
    main()


