#!/usr/bin/env python
usage = """Usage: embed x y z 
  Shows a 3d rendering of the MPI rank embedding used by
  S3D for the given dimensions. 
Parameters: 
  x   Number of processing elements in x direction
  y   Number of processing elements in y direction
  z   Number of processing elements in z direction
"""
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from vtk import *
from vtk.util.colors import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

zfactor = 1.5

class PointPlotter:
    def __init__(self):
        self.points = vtkPoints()
        self.scalars = vtkUnsignedCharArray()
        self.scalars.SetNumberOfComponents(3)
        self.color = (0,0,0)
        self.radius = 0.05
        
    def set_color(self, color):
        self.color = color

    def set_radius(self, radius):
        self.radius = radius

    def plot(self, p, color=None):
        if not color:
            color = self.color
        self.points.InsertNextPoint(p[0], p[1], p[2])
	self.scalars.InsertNextTuple3(color[0], color[1], color[2])
        
    def create_poly_data(self):
        ball = vtkSphereSource()
        ball.SetRadius(self.radius)
        ball.SetThetaResolution(12)
        ball.SetPhiResolution(12)

	polyData = vtkPolyData()
	polyData.SetPoints(self.points)
	polyData.GetPointData().SetScalars(self.scalars)
        
	balls = vtkGlyph3D()
	balls.SetSourceConnection(ball.GetOutputPort())
	balls.SetInput(polyData)

	balls.SetColorModeToColorByScalar()
	balls.SetScaleModeToDataScalingOff()

	return balls.GetOutput()

    def create_actor(self):
	polyData = self.create_poly_data()
	mapper = vtkPolyDataMapper()
	mapper.SetInput(polyData);

	actor = vtkActor()
        actor.GetProperty().SetSpecularColor(1, 1, 1)
        actor.GetProperty().SetSpecular(0.3)
        actor.GetProperty().SetSpecularPower(10)
        actor.GetProperty().SetAmbient(0.2)
        actor.GetProperty().SetDiffuse(0.8)

	actor.SetMapper(mapper);
        return actor


class LinePlotter:
    def __init__(self):
        self.points = vtkPoints()
        self.lines = vtkCellArray()
        self.scalars = vtkFloatArray()
        self.scalars.SetNumberOfComponents(1)
        self.set_scalar_range(0, 1)
        self.color = 0
        self.lookup = vtkLookupTable()
        self.id = 0

    def set_scalar_range(self, min, max):
        self.scalar_min = min
        self.scalar_max = max
        
    def set_lookup_table(self, table):
        self.lookup = table

    def set_color(self, color):
        self.color = color

    def plot(self, m, n, color=None):
        if not self.color:
            color = self.color

        self.points.InsertNextPoint(m)
	self.scalars.InsertNextTuple1(color)

	self.points.InsertNextPoint(n)
	self.scalars.InsertNextTuple1(color)

	self.lines.InsertNextCell(2);
	self.lines.InsertCellPoint(self.id)
	self.lines.InsertCellPoint(self.id+1)
        self.id += 2

    def create_poly_data(self):
	polyData = vtkPolyData()
	polyData.SetPoints(self.points)
        polyData.SetLines(self.lines)
	polyData.GetPointData().SetScalars(self.scalars)
	return polyData

    def create_actor(self):
        polyData = self.create_poly_data()
		
        tubes = vtkTubeFilter()
        tubes.SetInput(polyData)
        tubes.SetRadius(0.01)
        tubes.SetNumberOfSides(6)

	mapper = vtkPolyDataMapper()
	mapper.SetInput(tubes.GetOutput())
	mapper.SetLookupTable(self.lookup)
	mapper.SetColorModeToMapScalars()
	mapper.SetScalarRange(self.scalar_min, self.scalar_max)
	mapper.SetScalarModeToUsePointData()

	actor = vtkActor()
	actor.SetMapper(mapper)
        actor.GetProperty().SetColor(peacock)
        actor.GetProperty().SetSpecularColor(1, 1, 1)
        actor.GetProperty().SetSpecular(0.3)
        actor.GetProperty().SetSpecularPower(20)
        actor.GetProperty().SetAmbient(0.2)
        actor.GetProperty().SetDiffuse(0.8)

	return actor



def s3d_point_fun(rank, npx, npy, npz):
    z = rank / (npx*npy)
    x = (rank - (z*npx*npy)) % npx
    y = (rank - (z*npx*npy)) / npx
    
    return (x,y,zfactor*z)
    

def create_topology(topo_fun, npx, npy, npz):
    """Creates an actor for the given topology"""
    size = npx * npy * npz

    r = 0.05    
    points = PointPlotter()
    points.set_radius(r)

    lines = LinePlotter()

    plot_fun = s3d_point_fun
    prev = plot_fun(0, npx, npy, npz)
    points.plot(prev)

    for i in xrange(1,size):
        cur = plot_fun(i, npx, npy, npz)
        points.plot(cur)
        lines.plot(prev, cur)
        prev = cur
        
    topo = vtkPropAssembly()
    topo.AddPart(points.create_actor())
    topo.AddPart(lines.create_actor())
    
    cube = vtkCubeSource()
    cube.SetBounds(0-r, npx-1+r, 0-r, npy-1+r, 0-r, zfactor * (npz-1)+r)

    mapper = vtkPolyDataMapper()
    mapper.SetInput(cube.GetOutput())
    cube_actor = vtkActor()
    cube_actor.SetMapper(mapper)
    cube_actor.GetProperty().SetColor(peacock)
    cube_actor.GetProperty().SetOpacity(.35)
    topo.AddPart(cube_actor)

    return (topo, cube)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print usage
        sys.exit(1)

    app = QApplication(sys.argv)
    def finalize():
        app.quit()
    app.connect(app, SIGNAL( 'lastWindowClosed()' ), finalize);

    mainWindow = QMainWindow()
    vtkFrame = QVTKRenderWindowInteractor(mainWindow)
    mainWindow.setCentralWidget(vtkFrame)

    renderer = vtkRenderer()
    renderer.SetBackground(1,1,1)
    vtkFrame.GetRenderWindow().AddRenderer(renderer)

    npx, npy, npz = map(lambda x: int(x), sys.argv[1:4])
    
    topo, cube = create_topology(s3d_point_fun, npx, npy, npz)
    renderer.AddActor(topo)

    axes = vtkCubeAxesActor2D()
    axes.SetCamera(renderer.GetActiveCamera())
    axes.SetFlyModeToOuterEdges()
    
    tprop = vtkTextProperty()
    tprop.SetColor(0,0,0)

    axes.SetLabelFormat("%6.4g")
    axes.SetFontFactor(0.8)
    axes.SetAxisTitleTextProperty(tprop)
    axes.SetAxisLabelTextProperty(tprop)
    axes.SetXLabel("x")
    axes.SetYLabel("y")
    axes.SetZLabel("z")
    axes.SetInput(cube.GetOutput())
    axes.GetProperty().SetColor(black)

    axes.GetXAxisActor2D().SetLabelVisibility(0)
    axes.GetYAxisActor2D().SetLabelVisibility(0)
    axes.GetZAxisActor2D().SetLabelVisibility(0)

    renderer.AddViewProp(axes)

    mainWindow.resize(1024, 768)
    mainWindow.move(50, 50)

    renderer.ResetCamera()

    mainWindow.show()
    sys.exit(app.exec_())
