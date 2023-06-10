import json
import time

import pygame
from pygame.locals import *
from OpenGL.GLU import *
from OpenGL.GL import *

from modules.paths import *
from modules.color import color


class Scene:
    def __init__(self, hidden=False):
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600

        self.rotation_angle = 0.0
        self.scene_elements_last_modified = 0.0
        self.scene_elements_list: list = []

        pygame.init()

        if hidden:
            pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), HIDDEN | DOUBLEBUF | OPENGL)
        else:
            pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
            # pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.OPENGL)

        self.init_gl()

    def init_gl(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.WINDOW_WIDTH / self.WINDOW_HEIGHT), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def play_scene(self):
        quit_trigger = False
        while not quit_trigger:
            self.update_scene()
            pygame.time.delay(int(1000 / 60))
            quit_trigger = self.pygame_check_for_quit()
        pygame.quit()
        print("Rendering complete.")

    def update_scene(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.rotation_angle += 1.0

        glTranslatef(0.0, 0.0, -2.0)  # Move the triangle away from the camera
        glRotatef(self.rotation_angle, 1.0, 1.0, 1.0)  # Rotate the triangle

        self.update_scene_elements()

        for element in self.scene_elements_list:
            self.draw_element(element)

        pygame.display.flip()
        glFlush()

    def update_scene_elements(self) -> bool:
        try:
            # checking if scene elements file has changed or this function runs for the first time
            if self.scene_elements_last_modified != os.stat(SCENE_ELEMENTS_JSON_PATH).st_mtime:
                with open(SCENE_ELEMENTS_JSON_PATH, 'r') as file:
                    self.scene_elements_list = json.load(file)
                self.scene_elements_last_modified = os.stat(SCENE_ELEMENTS_JSON_PATH).st_mtime
                return True
        except json.decoder.JSONDecodeError:
            pass
        return False

    @staticmethod
    def draw_element(element: dict) -> None:
        if element['shape'] == 'triangle':
            glBegin(GL_TRIANGLES)
            for vertex in element['vertices']:
                # vertex color
                glColor3f(*color.get(vertex['color'], color['white']))
                # vertex coordinates
                glVertex3f(*(vertex['x_pos'], vertex['y_pos'], vertex['z_pos']))
            glEnd()

    def render_frame_to_file(self, frame_count: int) -> None:
        pixels = glReadPixels(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, GL_RGB, GL_UNSIGNED_BYTE)
        surface = pygame.image.fromstring(pixels, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT), 'RGB')
        pygame.image.save(surface, f"{FRAMES_DIR_PATH}/frame_{frame_count:04d}.png")

    def render_movie_frames(self, render_time: float) -> None:
        start_time = time.time()
        elapsed_time = 0.0
        frame_count = 0
        quit_trigger = False

        while elapsed_time < render_time and not quit_trigger:
            self.update_scene()
            self.render_frame_to_file(frame_count)
            frame_count += 1
            elapsed_time = time.time() - start_time
            quit_trigger = self.pygame_check_for_quit()

        pygame.quit()
        print(f"Saved {frame_count} frames as separate files.")

    @staticmethod
    def pygame_check_for_quit() -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
        return False
