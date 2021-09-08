from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np
from vector import Vector
import matplotlib as mpl
import matplotlib.cm as cm

# list(sns.color_palette("Spectral"))

class VectorField():
    def __init__(self, func_x , func_y,  n_points=10, x0=None, y0=None, xf=None, yf=None, axes=True, points=False, vectors=True, norm=False):
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
        self.grid_values = np.zeros((n_points, n_points, 2))

        self.func_x = func_x
        self.func_y = func_y

        self._update_field()

        if axes:
            self._draw_axes()
        if vectors:
            self._draw_vectors(norm)
        if points:
            self._draw_points()
        
        # self._draw_points()

    def _get_length(self, norm=True):
        def get_length(vector):
            vec_len = Vector(*vector,draw=False).length
            return vec_len
        
        get_length_vec = np.vectorize(get_length, signature="(2)->()")
        grid_length = get_length_vec(self.grid_values)
        # print(grid_length)

        if norm:
            grid_length /= grid_length.max()
        
        return grid_length

    def _get_colors(self, grid_length, max_value=None):

        if not max_value:
            max_value = grid_length.max()

        norm = mpl.colors.Normalize(vmin=0, vmax=max_value)
        cmap = cm.get_cmap('Spectral').reversed()
        m = cm.ScalarMappable(norm=norm, cmap=cmap)

        vec_color = m.to_rgba(grid_length, alpha=1)

        return vec_color

    
    def _update_field(self):
        # xi, yi = np.meshgrid(
        #     np.arange((-self.n_points//2)+1, (self.n_points//2)+1),
        #     np.arange((-self.n_points//2)+1, (self.n_points//2)+1),
        #     indexing='ij')

        # # x = self.func_x(xi[::-1], yi)
        # # y = self.func_y(xi[::-1], yi)
        # coord = np.dstack((xi[::-1],yi))
        # size_vec = np.vectorize(func, signature=("(i)->()"))

        for i, array in enumerate(self.grid_values):
            for j, vector in enumerate(array):
                x = j - (self.n_points//2)
                y = i - (self.n_points//2) 
                
                new_x = self.func_x(x, y)
                new_y = self.func_y(x, y) 
                self.grid_values[i][j] = np.array([new_x, new_y])

        
    
    def _draw_vectors(self, norm):      
        (x0, y0), _ = self.coordinates
        lengths = self._get_length(norm)
        colors = self._get_colors(lengths)

        for i, array in enumerate(self.grid_values):
            for j, vector in enumerate(array):
                offset = np.array([self.dx/2, self.dy/2])
                cell_pos = np.array([x0 + (self.dx * j), y0 + (self.dy * i)])
                pos = cell_pos + offset
                vector = self.grid_values[i][j]
                if norm:
                    length = lengths[i][j]
                else:
                    length = 0.8
                Vector(*vector,position=pos, size=self.dx * length, color=colors[i][j][:3])

    def _draw_points(self):
        (x0, y0), _ = self.coordinates

        for i, array in enumerate(self.grid_values):
            for j, vector in enumerate(array):
                offset = np.array([self.dx/2, self.dy/2])
                cell_pos = np.array([x0 + (self.dx * j), y0 + (self.dy * i)])
                pos = cell_pos + offset
                
                glBegin(GL_POINTS)
                glColor3fv((255,255,255))
                glVertex3f(pos[0],pos[1],0)
                glEnd()
                # Vector(1,0,position=pos, size=self.dx - 15)
    
    
    def _draw_axes(self):
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
    
    def get_vector_from_pos(self, x, y):
        (x0, y0), (xf, yf) = self.coordinates

        if (x > x0 and x < xf) and (y > y0 and y < yf):
            i = int(np.floor(y /self.dy)) + int(self.n_points/2)
            j = int(np.floor(x /self.dx)) + int(self.n_points/2)
            return self.grid_values[i][j]
        else:
            # print("Erro:",x,y)
            return None