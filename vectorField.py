from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np
from vector import Vector

class VectorField():
    def __init__(self, func_x , func_y,  n_points=10, x0=None, y0=None, xf=None, yf=None, axes=True, points=True, square=True):
        # Canvas
        coordinates = [x0, xf, y0, yf]
        if all(coordinates):
            print("entrou")
            self.coordinates = ((x0,y0),(xf,yf))
        else:
            w = glutGet(GLUT_WINDOW_WIDTH)
            h = glutGet(GLUT_WINDOW_HEIGHT)
            self.coordinates = ((-w,-h),(w,h))

        # Cell size
        if n_points:
            self.n_points = n_points

            (x0, y0), (xf, yf) = self.coordinates
            self.dx = (xf - x0)/n_points
            self.dy = (yf - y0)/n_points
        else:
            raise Exception("Must pass n_points or cell size.")

        # Grid
        self.grid_values = np.zeros((n_points, n_points))

        self.func_x = func_x
        self.func_y = func_y

        if axes:
            self._plot_axes()

        self.draw()


    def _update_field(self):
        xi, yi = np.meshgrid(
            np.arange(-self.n_points/2, (self.n_points/2)+1),
            np.arange(-self.n_points/2, (self.n_points/2)+1),
            indexing='ij')
        
        x = self.func_x(xi[::-1], yi)
        y = self.func_y(xi[::-1], yi)

        return np.dstack((x,y))
    
    def draw(self):
        # self.grid_values = self._update_field()      
        (x0, y0), _ = self.coordinates

        for j, array in enumerate(self.grid_values):
            for i, vector in enumerate(array):
                pos = (x0 + (self.dx * i), y0 + (self.dy * j))
                # print(vector, pos)
                Vector(1,1,position=pos, size=100)

    def _plot_axes(self):
        (x0, y0), (xf, yf) = self.coordinates

        x_mid = ((xf-x0)/2) + x0
        y_mid = ((yf-y0)/2) + y0

        axes_points = [
            ( x0   , y_mid, 0),
            ( xf   , y_mid, 0),
            ( x_mid, y0   , 0),
            ( x_mid, yf   , 0),
            # (0    , 0     , 0),
            # (0    , 0     , 0),
        ]

        glBegin(GL_LINES)
        glColor3fv((255,255,255))
        for i in range(len(axes_points)):
            glVertex3fv(axes_points[i])
        glEnd()