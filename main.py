import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time

# Window dimensions
width = 800
height = 600

rotation_angle = 0.0

def draw_triangle():
    global rotation_angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    glTranslatef(0.0, 0.0, -2.0)  # Move the triangle away from the camera
    glRotatef(rotation_angle, 1.0, 1.0, 1.0)  # Rotate the triangle
    
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)  # Red
    glVertex3f(0.0, 0.6, 0.0)
    
    glColor3f(0.0, 1.0, 0.0)  # Green
    glVertex3f(-0.5, -0.5, 0.5)
    
    glColor3f(0.0, 0.0, 1.0)  # Blue
    glVertex3f(0.5, -0.5, 0.0)
    glEnd()
    
    glFlush()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width / height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def update():
    global rotation_angle
    rotation_angle += 1.0

def main():
    pygame.init()
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
        
        update()
        draw_triangle()
        pygame.display.flip()
        time.sleep(0.01)

if __name__ == '__main__':
    main()
