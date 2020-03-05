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

def get_polydata(iqdata):
    rawiq = np.fromfile(iqdata, dtype='f', count = -1)
    point_count = int(rawiq.size/2)
    iqtwo = rawiq.reshape(point_count, 2)
    iqtwo = iqtwo*100000 #scale the IQ data
    #z = np.arange(point_count)
    z = np.arange(0,100000,100000/point_count)  
    iqthree = np.column_stack((iqtwo,z))
    #print(str(rawiq[0]), str(rawiq[1])) #sanity check

    #plot just I data in 2d and extend the array
    qaxis = np.zeros(point_count)
    i2data = np.column_stack((qaxis,iqtwo[:,0] ))
    idata = np.column_stack((i2data, z))
    iq_with_iaxis = np.append(iqthree,idata)

    vtkdata = numpy_support.numpy_to_vtk(iq_with_iaxis, deep=False, array_type=vtk.VTK_FLOAT)
    vtkdata.SetNumberOfComponents(3)
    vtkdata.SetName("Points")


    #idatavtk = numpy_support.numpy_to_vtk(idata, deep=False, array_type=vtk.VTK_FLOAT)
    #idatavtk.SetNumberOfComponents(3)
    #idatavtk.SetName("Idata")
    #table = vtk.vtkTable
    #table.addColumn(vtkdata)
    #lines = vtk.vtkCellArray()
    #for p in range(point_count-1):
    #    line = vtk.vtkLine()
    #    line.GetPointIds().SetId(0,p)
    #    line.GetPointIds().SetId(0,p+1)
    #    lines.InsertNextCell(line)
    points = vtk.vtkPoints()
    points.SetData(vtkdata)
    pd = vtk.vtkPolyData()
    pd.SetPoints(points)
    pd.GetPointData().AddArray(vtkdata)
    #pd.GetPointData().AddArray(idatavtk)
    vg = vtk.vtkVertexGlyphFilter()
    vg.SetInputData(pd)
    vg.Update()
    poly = vg.GetOutput()
    #poly.SetLines(lines)


def viewdata():
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(normals.GetOutput())
    mapper.ScalarVisibilityOn()
    mapper.SetScalarRange(-1,1)
    mapper.SetScalarModeToUsePointFieldData()
    mapper.ColorByArrayComponent("Velocity", 0)
    #print image
    #print contour

    #mapper.SelectColorArray("Q-criterion")
    #mapper.SetLookupTable(lut)

    print mapper
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground(1,1,1)
    ren.ResetCamera()

    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(600,600)
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    def MouseMove(self, data):
        print("Load Cache %s" % data )
        print ("Iren data")
        #print iren
        #addcube
        #print ren
        print ren.GetViewPoint()
        print ren.GetDisplayPoint()
        print ren.WorldToView()
        print ren.ComputeVisiblePropBounds()
        ysize = renWin.GetSize()[1]
        c.SetValue(0,ysize)
        c.Update()
        normals = vtk.vtkPolyDataNormals()
        normals.SetInputData(c.GetOutput())
        normals.SetFeatureAngle(25) #?
        normals.Update()

        normals.SetFeatureAngle(45) #?
        normals.Update()
        mapper2 = vtk.vtkPolyDataMapper()
        mapper2.SetInputData(normals.GetOutput())
        mapper2.ScalarVisibilityOn()
        mapper2.SetScalarRange(-.5,1)
        mapper2.SetScalarModeToUsePointFieldData()
        mapper2.ColorByArrayComponent("Velocity", 0)
        actor2 = vtk.vtkActor()
        actor2.SetMapper(mapper2)
        ren.AddActor(actor2)

 
    iren.AddObserver("MiddleButtonPressEvent", MouseMove)

    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()

def main():
    iqdata, outfile = get_files()
    polydata = get_polydata(iqdata)
    
    w = vtk.vtkXMLPolyDataWriter()
    w.SetInputData(poly)
    w.SetFileName("autotest.vtp")
    w.Write()
    #pdb.set_trace()
    outfile.close()    
    iqdata.close()

if __name__ == '__main__':
    main()


