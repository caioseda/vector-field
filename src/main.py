from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np
from vector import Vector
from vectorField import VectorField

N_PONTOS = 20
WIDTH = 1080
HEIGHT = 1080
CELL_SIZE = 20

z = -2
angulo_rot = 1

def draw(): 
    global z, angulo_rot
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    
    glPushMatrix()
    # vec = Vector(1,1, size=100)
    # vec = Vector(2,-9, size=200)
    
    # V = VectorField(10, -600, -600, 600, 600)
    func_x = lambda x,y: x**2 - y**2 - 64
    func_y = lambda x,y: 2*x*y
    # V = VectorField(func_x, func_y, 51,vectors=True)
    
    # c) Vx(x,y)=4cos(y / 3 + p / 4); Vy(x,y)=4sin(x / 3 + p / 4)

    # func_x = lambda x,y: 4 * np.cos((y/3)+(x/4))
    # func_y = lambda x,y: 4 * np.sin((x/3)+(y/4))
    V = VectorField(func_x, func_y, 25 ,vectors=True, norm=False)
    # V pip l VectorField(lambda x, y: x, lambda x, y: -y, 31,vectors=True)
    glPopMatrix()

    glutSwapBuffers() #Não sei o que faz

    angulo_rot += 2

def curve(V, x,y, step, num_steps):
    p = np.array([x,y])

    glBegin(GL_LINE_STRIP)
    glColor3f(0,255,0)
    glVertex3f(*p,0)
    for i in range(num_steps):
        vector = V.get_vector_from_pos(*p)
        if vector is not None:
            # print(i,"v",p, vector, step, vector * step, p + (vector * step))
            p = p + (vector * step)
            glVertex3f(*p,0)
            
    glEnd()       



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
# gluOrtho2D(-6,6,-6,6)
gluOrtho2D(-800,800,-800,800)
# glTranslatef(0.0,0.0,-20)
glutTimerFunc(50,timer,1)
glutMainLoop()

