# Notes for installation on Fedora 31

## VTK Installation

```
$ sudo dnf install vtk python3-vtk
```

## Paraview Installation

### Required Packages

- `mesa-libGLU`

### Install

```
$ wget https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v5.8&type=binary&os=Linux&downloadFile=ParaView-5.8.0-MPI-Linux-Python3.7-64bit.tar.gz
$ tar xvzf ParaView-5.8.0-MPI-Linux-Python3.7-64bit.tar.gz
$ sudo mv ParaView-5.8.0-MPI-Linux-Python3.7-64bit.tar.gz /opt
```

