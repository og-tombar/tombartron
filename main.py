# libraries
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time

# custom modules
from modules.all_utils import *

# Window dimensions
width = 800
height = 600

rotation_angle = 0.0
render_time = 2.0
output_prefix = "frame_"

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

def render_to_frames(output_prefix):
    pygame.init()
    pygame.display.set_mode((width, height), HIDDEN | DOUBLEBUF | OPENGL)
    init()

    start_time = time.time()
    elapsed_time = 0.0
    frame_count = 0

    while elapsed_time < render_time:
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

        # Save the current frame as an image file
        pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        surface = pygame.image.fromstring(pixels, (width, height), 'RGB')
        pygame.image.save(surface, f"{FRAMES_DIR_PATH}/{output_prefix}{frame_count:04d}.png")

        frame_count += 1
        elapsed_time = time.time() - start_time

    pygame.quit()

    print(f"Saved {frame_count} frames as separate files.")

if __name__ == '__main__':
    render_to_frames(output_prefix)
