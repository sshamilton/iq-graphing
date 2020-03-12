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
    parser.add_argument('-s', '--samplerate', dest='sample_rate',
            type=float, nargs='?', required=True,
            help='sample rate in Msps, ex. 1.8 = 1.8Msps')
    parser.add_argument('-z', '--zscale', dest='zscale',
            type=float, default=10.0, nargs='?', required=False,
            help='scale factor for z-axis (time)')
    parser.add_argument('--project_i', dest='project_i', action='store_true',
            help='project the I (real) portion of the signal')
    parser.set_defaults(project_i=False)
    parser.add_argument('--project_q', dest='project_q', action='store_true',
            help='project the Q (imaginary) portion of the signal')
    parser.set_defaults(project_q=False)

    return parser.parse_args()

def get_data(infile):
    print("Processing file ", infile)
    try:
        iqdata = open(infile, "rb")
    except Exception as e:
        print("Unable to open ", infile)
        print ("Exception is: ", e)
    return iqdata 

def decimate(data, rate):
    return [ i for i,j in zip(data,range(len(data))) if not j%rate ] 

def print_sanity_check(data, name):
    print("*** sanity check for {}: \n\ttype: {}\n\tlen()={}\n\t[0]={}\n\t[-1]={}".format(
        name, str(type(data)), len(data), data[0], data[-1])) # sanity check

def print_arr_stats(arr, name):
    print("*** Stats for {}:\n\tmax={}\n\tmin={}\n\tmean={}\n\telements={}".format(
        name, arr.max(), arr.min(), arr.mean(), arr.size))

# add a projection for i or q onto the numpy array
# returns a new n-dim array with the projection data included
def gen_projection(target, offset, arr, num_samples):
    offset_arr = np.zeros(num_samples)
    offset_arr.fill(offset)
    if target == 'i':
        projection = np.column_stack((arr[:,0], offset_arr, arr[:,2]))
        return projection
    if target == 'q':
        projection = np.column_stack((offset_arr, arr[:,1], arr[:,2]))
        return projection


def get_polydata(iqdata, sample_rate, zscale, project_i, project_q):
    # read data as numpy array, from file, datatype=float, count=allitems
    # TODO: grqx uses gnuradio lib to pack data as complex64 IEEE 754 format
    # this should be able to be parsed with the np.complex64
    iq = np.fromfile(iqdata, dtype='complex64', count = -1)
    print_sanity_check(iq, "iq")

    print_arr_stats(iq.real, "iq.real")
    print_arr_stats(iq.imag, "iq.imag")

    # Generate time (z-axis)
    num_samples = iq.size
    # sample_rate is in Msps so multiply by 1000000
    z = [ i/(sample_rate*1000000) for i in range(0,num_samples) ]
    print(z[0])
    #print_sanity_check(z, "z")
    #print_arr_stats(z, "z")


    # grab real/imag components for vtk
    iqz = np.column_stack((
            np.array(iq.real, dtype=float), 
            np.array(iq.imag, dtype=float),
            np.array(z, dtype=float)*zscale))
    print_sanity_check(iqz, "iqz")
    
    # scale real/imag components up
    print("*** iqz[:,0] = {}".format(iqz[:,0]))
    maxmag = max(abs(iqz[:,0].max()), abs(iqz[:,0].min()), abs(iqz[:,1].max()), abs(iqz[:,1].min()))
    print("*** maxmag is {}".format(maxmag))
    
    scalefactor = (1 / maxmag)
    print("*** scale value = {}".format(scalefactor))

    iqz[:,0] *= scalefactor
    iqz[:,1] *= scalefactor 

    #print_sanity_check(iqz, "iqz post scaling")

    # build projections
    iqz_final = iqz
    if project_i:
        iqz_final = np.append(iqz_final, gen_projection('i', 2*maxmag*scalefactor, iqz, num_samples))
    if project_q:
        iqz_final = np.append(iqz_final, gen_projection('q', 2*maxmag*scalefactor, iqz, num_samples))
   
    # Produce vtk data
    vtkdata = numpy_support.numpy_to_vtk(iqz_final, deep=False, array_type=vtk.VTK_FLOAT)
    vtkdata.SetNumberOfComponents(3)
    vtkdata.SetName("Points")

    points = vtk.vtkPoints()
    points.SetData(vtkdata)


    pd = vtk.vtkPolyData()
    pd.SetPoints(points)
    pd.GetPointData().AddArray(vtkdata)

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

def print_process_info(args):
    print("Transforming Data for use in VTK")
    print("  - Input file: {}".format(args.input_file))
    print("  - Output file: {}".format(args.output_file))
    print("  - Sample Rate: {} Msps".format(args.sample_rate))
    print("  - zscale: {}".format(args.zscale))

def main():
    # get cmd line args
    args = get_args()

    # print process information
    print_process_info(args)

    # process raw data for iq values
    iqdata = get_data(args.input_file)

    polydata = get_polydata(
            iqdata, 
            args.sample_rate, 
            args.zscale, 
            args.project_i,
            args.project_q)
    
    w = vtk.vtkXMLPolyDataWriter()
    w.SetInputData(polydata)
    w.SetFileName(args.output_file)
    w.Write()
    #Now bring up the 3d Viewer
    #viewdata(polydata)
    iqdata.close()

if __name__ == '__main__':
    main()


