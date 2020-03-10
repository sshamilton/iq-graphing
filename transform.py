#!/usr/bin/env python3

#program to convert raw IQ file to VTK Polydata.
# Written by Stephen Hamilton 
# 2 Jan 2020

import sys
import struct
import math
import vtk
import numpy as np
from vtk.util import numpy_support
import argparse


# Argument parsing
def get_args():
    parser = argparse.ArgumentParser(description="convert raw data to vtk or csv")
    parser.add_argument('-i', '--inputfile', dest='input_file',
            type=str, nargs='?', required=True,
            help='Input file to convert, should be raw capture')
    parser.add_argument('-o', '--outputfile', dest='output_file',
            type=str, nargs='?', required=True,
            help='output filename')
    return parser.parse_args()

def get_data(infile):
    print("Processing file ", infile)
    try:
        iqdata = open(infile, "rb")
    except Exception as e:
        print("Unable to open ", infile)
        print ("Exception is: ", e)
    return iqdata 

def get_polydata(iqdata):
    # read data as numpy array, from file, datatype=float, count=allitems
    rawiq = np.fromfile(iqdata, dtype='f', count = -1)

    # create 2d array of iq points
    point_count = int(rawiq.size/2)
    iqtwo = rawiq.reshape(point_count, 2)


    scale = 10000000
    iqtwo = iqtwo*scale #scale the IQ data

    #z = np.arange(point_count)
    zscale = scale*10
    #z = np.arange(0,zscale,zscale/(point_count))  
    z = np.arange(0,len(iqtwo))
    #iqthree = np.column_stack((iqtwo,z))
    iqthree = np.column_stack((iqtwo,z))
    print("Raw iq 0: "+str(rawiq[0])+" Raw iq 1: "+ str(rawiq[1])) #sanity check
    print("Raw iq end: "+str(rawiq[-1])+" Raw iq end: "+ str(rawiq[-1])) #sanity check
    print("iqthree 0: "+str(iqthree[0])+" iqthree 1: "+ str(iqthree[1])) #sanity check
    print("iqthree end: "+str(iqthree[-1])+" iqthree end: "+ str(iqthree[-1])) #sanity check
    print("Number of samples: "+str(len(iqthree)))

    #plot just I data in 2d and extend the array
    qaxis = np.zeros(point_count)
    qaxis.fill((-1*scale)/10)
    i2data = np.column_stack((iqtwo[:,0],qaxis ))
    idata = np.column_stack((i2data, z))
    iq_with_iaxis = np.append(iqthree,idata)

    #plot just Q data in 2d and extend the array
    q2data = np.column_stack((qaxis,iqtwo[:,1] ))
    qdata = np.column_stack((q2data,z))
    iq_with_iqaxis = np.append(iq_with_iaxis,qdata)

    vtkdata = numpy_support.numpy_to_vtk(iqthree, deep=False, array_type=vtk.VTK_FLOAT)
    vtkdata.SetNumberOfComponents(3)
    vtkdata.SetName("Points")

    points = vtk.vtkPoints()
    points.SetData(vtkdata)


    pd = vtk.vtkPolyData()
    pd.SetPoints(points)
    pd.GetPointData().AddArray(vtkdata)
    #attempt to draw lines between points
    lines = vtk.vtkCellArray()
    #for i in range(0,point_count-1):
    #    line = vtk.vtkLine()
    #    line.GetPointIds().SetId(0,i+1)
    #    line.GetPointIds().SetId(1,i+2)
    #    lines.InsertNextCell(line)

    pd.SetLines(lines)
    vg = vtk.vtkVertexGlyphFilter()
    vg.SetInputData(pd)
    vg.Update()
    poly = vg.GetOutput()

    return poly

# draw image with python
def viewdata(polydata):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    #mapper.ScalarVisibilityOn()
    #mapper.SetScalarRange(-100,100)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground(0,0,0)
    ren.ResetCamera()

    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(1024,1024)
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    def MouseMove(self, data):
        print("Load Cache %s" % data )
        print ("Iren data")
        #print iren
        #addcube
        #print ren
        #print ren.GetViewPoint()
        #print ren.GetDisplayPoint()
        #print ren.WorldToView()
        #print ren.ComputeVisiblePropBounds()
        ysize = renWin.GetSize()[1]
        c.SetValue(0,ysize)
        c.Update()
        #mapper2 = vtk.vtkPolyDataMapper()
        #mapper2.SetInputData(polydata)
        #mapper2.ScalarVisibilityOn()
        #mapper2.SetScalarRange(-100,100)
        #actor2 = vtk.vtkActor()
        #actor2.SetMapper(mapper2)
        #ren.AddActor(actor2)

 
    iren.AddObserver("MiddleButtonPressEvent", MouseMove)

    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()

def main():
    # get cmd line args
    args = get_args()

    # process raw data for iq values
    iqdata = get_data(args.input_file)

    # 
    polydata = get_polydata(iqdata)
    
    w = vtk.vtkXMLPolyDataWriter()
    w.SetInputData(polydata)
    w.SetFileName(args.output_file)
    w.Write()
    #Now bring up the 3d Viewer
    #viewdata(polydata)
    iqdata.close()

if __name__ == '__main__':
    main()


