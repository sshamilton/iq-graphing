# iq-graphing

These are two scripts to assist with IQ data transformation for 
visualization in VTK.  One converts it to CSV for import, while the other
creates a native VTK file for viewing directly.# Notes for installation on Fedora 31


## Installation: Fedora 31

### VTK Installation

```
$ sudo dnf install vtk python3-vtk
```

### Paraview Installation


- Get required packages:
```
$ sudo dnf install mesa-libGLU
```

- Get Paraview and install to `/opt`
```
$ wget https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v5.8&type=binary&os=Linux&downloadFile=ParaView-5.8.0-MPI-Linux-Python3.7-64bit.tar.gz
$ tar xvzf ParaView-5.8.0-MPI-Linux-Python3.7-64bit.tar.gz
$ sudo mv ParaView-5.8.0-MPI-Linux-Python3.7-64bit.tar.gz /opt
```

