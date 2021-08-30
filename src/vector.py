from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

class Vector():
    def __init__(self, x=None, y=None, position=(0,0), angle=None, size=1):
        
        self.v = np.array([1,0])
        self.position = np.array(position)
        
        if x != None and y != None:
            self.angle = self._get_angle(x,y)
            self.length = self._get_length(x,y)
        elif angle != None:
            self.angle = angle
            self.length = 1
        else:
            raise Exception('You must pass x and y, or, angle and size.')

        self.size = size

        self.draw()
   
    def _get_angle(self, x, y):
        return np.degrees(np.arctan2(y,x))

    def _get_length(self, x, y):
        return np.sqrt(y**2 + x**2)

    def draw_vector(self):        
        glBegin(GL_LINES)
        glColor3f(255,255,255)
        glVertex3f(0,0,0)
        glVertex3f(self.v[0], self.v[1],0)
        glEnd()

        arrow_head_x = self.v[0]* 0.85
        arrow_head_y = self.v[0] - arrow_head_x

        glBegin(GL_TRIANGLES)
        glVertex3f(self.v[0], self.v[1],0)
        glVertex3f(arrow_head_x, arrow_head_y,0)
        glVertex3f(arrow_head_x, - arrow_head_y,0)
        glEnd()
        
    
    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.position[0],self.position[1],0)
        glScalef(self.size, self.size, 0)
        glRotatef(self.angle,0,0,1)
        
        # Vector center onto point
        glTranslatef(-self.v[0]/2, -self.v[1]/2, 0)

        self.draw_vector()

        glPopMatrix()