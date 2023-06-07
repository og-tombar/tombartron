import pygame
from OpenGL.GL import *

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


def update_scene():
    global rotation_angle
    rotation_angle += 1.0
    draw_triangle()
    pygame.display.flip()
    glFlush()
