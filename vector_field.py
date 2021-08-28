from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

N_PONTOS = 20
WIDTH = 1080
HEIGHT = 1080
CELL_SIZE = 20

z = -2
angulo_rot = 0

class Vector():
    def __init__(self, x, y, angle=0, size=1, default_vector=None):
        if default_vector:
            self.v = default_vector 
        else:
            self.v = np.array([1,0])
        
        self.position = np.array([x,y])
        self.angle = angle
        self.size = size

        self.default_vector = default_vector
    
    def draw_vector(self, head_angle=90):        
        glBegin(GL_LINES)
        glVertex3f(0,0,0)
        glVertex3f(self.v[0], self.v[1],0)
        glEnd()

        scale_x = self.v[0]*0.85
        scale_y = self.v[1]*0.85
        m = -1/(self.v[0]/self.v[1])
        
        arrow_head_x1 = scale_x
        arrow_head_y1 = m * scale_x

        # arrow_head_x1 = np.cos(head_angle * scale_x)  - np.sin(head_angle * scale_y) 
        # arrow_head_y1 = np.sin(head_angle * scale_x)  + np.cos(head_angle * scale_y)
        
        # arrow_head_x2 = np.cos(-head_angle) * scale_x - np.sin(-head_angle) * scale_y
        # arrow_head_y2 = np.sin(-head_angle) * scale_x - np.cos(-head_angle) * scale_y

        glBegin(GL_POINTS)
        glVertex3f(self.v[0],self.v[1],0)
        glVertex3f(arrow_head_x1, arrow_head_y1,  0)
        glVertex3f(-arrow_head_x1, -arrow_head_y1,  0)
        glEnd()
    
    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.position[0],self.position[1],0)
        glScalef(self.size, self.size, 0)
        glRotatef(self.angle,0,0,1)
        glTranslatef(-self.v[0]/2, -self.v[1]/2, 0)

        self.draw_vector()

        glPopMatrix()
        

class VectorField():
    def __init__(self, n_points=10, cell_size=None, x0=None, xf=None, y0=None, yf=None):
        coordinates = [x0, xf, y0, yf]
        if all(coordinates):
            self.coordinates = ((x0,y0),(xf,yf))
        else:
            w = glutGet(GLUT_WINDOW_WIDTH)
            h = glutGet(GLUT_WINDOW_HEIGHT)
            self.coordinates = ((-w/2,-h/2),(w/2,h/2))

        if n_points:
            self.n_points = n_points
        elif cell_size:
            cell_size            
        else:
            raise Exception("Must pass n_points or cell size.")

        self.grid_values = np.matrix((n_points, n_points))


def draw():
    global z, angulo_rot
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()

    Vector(1,1).draw()
    # draw_axes(5,5,5)
    # draw_pontos(N_PONTOS, 800,-800,800,-800)

    # draw_grid(draw_vector, N_PONTOS, 5,-5,5,-5)
    # draw_vector(1,1, angle =45, size=.5)

    glPopMatrix()
    glutSwapBuffers() #Não sei o que faz


def vector(v,size):
    # v = np.array([1,0]) 
    
    glBegin(GL_LINES)
    glVertex3f(0,0,0)
    
    glVertex3f(v[0],v[1],0)
    glEnd()

    arrow_head_x = v[0]*0.85
    arrow_head_y = v[0] - arrow_head_x

    glBegin(GL_TRIANGLES)
    glVertex3f(v[0],v[1],0)
    glVertex3f(arrow_head_x,v[1] + arrow_head_y,0)
    glVertex3f(arrow_head_x,v[1] - arrow_head_y,0)
    glEnd()
    

def draw_vector(x, y, angle=0, size=1):
    v = np.array([1,0]) 
    position = np.array([x,y])

    glPushMatrix()
    glTranslatef(position[0],position[1],0)
    glScalef(size, size, 0)
    glRotatef(angle,0,0,1)
    glTranslatef(-v[0]/2, -v[1]/2, 0)

    vector(v, size)
    glPopMatrix()


def draw_grid(func, n, x0, xf, y0, yf):
    dx = (xf - x0)/n
    dy = (yf - y0)/n

    for i in range(n):
        y = y0 + dy*i

        for j in range(n):
            x = x0 + dx*j
            
            new_angle = (i/n) * 180
            func(x,y, angle=new_angle, size= dx*0.8)

def draw_pontos(n, x0, xf, y0, yf):
    dx = (xf - x0)/n
    dy = (yf - y0)/n

    glBegin(GL_POINTS)
    for i in range(n):
        y = y0 + dy*i

        for j in range(n):
            z = 0
            x = x0 + dx*j
            glVertex3f(x,y,z)
    glEnd()

def draw_axes(x_size, y_size, z_size):
    glBegin(GL_LINES)
    line = [
         ( 0, x_size, 0),
         ( 0,-x_size, 0),
         ( y_size, 0, 0),
         (-y_size, 0, 0),
         (0, 0, z_size),
         (0, 0, -z_size),
     ]
    for i in range(len(line)):
        glVertex3fv(line[i])
        glColor3fv((255,255,255))
    glEnd()


def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

def mouse(botao, estado, x, y):
    print(botao, estado, x, y)

def mouseMove(x, y):
    print(x, y)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH ) # |GLUT_MULTISAMPLE
glutInitWindowSize(800,800)
glutCreateWindow("Vector Field")
glutDisplayFunc(draw)
glutMotionFunc(mouseMove)
glutMouseFunc(mouse)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)

# gluPerspective(45,800.0/800.0,0.1,100.0)
gluOrtho2D(-6,6,-6,6)
# gluOrtho2D(-800,800,-800,800)
# glTranslatef(0.0,0.0,-20)
glutTimerFunc(50,timer,1)
glutMainLoop()

