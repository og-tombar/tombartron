import json
import time

import pygame
from pygame.locals import *
from OpenGL.GLU import *

from modules.paths import *
from modules.shapes import *
from modules.camera import Camera
from modules.light import Light


class Scene:
    def __init__(self, hidden=False):
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600

        self.scene_elements_last_modified = 0.0
        self.scene_elements_list: list = []

        pygame.init()

        if hidden:
            pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), HIDDEN | DOUBLEBUF | OPENGL)
        else:
            pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
            # full screen:
            # pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.OPENGL)

        self.init_gl()
        self.camera = Camera()
        self.light = Light()

    def init_gl(self) -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # TODO: Change this to address full screen as well?
        gluPerspective(45, (self.WINDOW_WIDTH / self.WINDOW_HEIGHT), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def play_scene(self) -> None:
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

        self.camera.update()
        self.light.activate()
        self.update_scene_elements()

        # temp
        self.scene_elements_list[0]['rotation']['yaw'] += 0.1
        self.scene_elements_list[0]['rotation']['pitch'] += 1
        self.scene_elements_list[0]['rotation']['roll'] += 0.1

        for element in self.scene_elements_list:
            self.create_element(element)

        self.light.deactivate()

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
    def create_element(element: dict) -> None:
        element = PolyhedronFactory.construct(element)
        glPushMatrix()
        element.pre_process()
        element.draw()
        glPopMatrix()

    def render_frame_to_file(self, frame_count: int) -> None:
        pixels = glReadPixels(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, GL_RGB, GL_UNSIGNED_BYTE)
        surface = pygame.image.fromstring(pixels, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT), 'RGB')
        if not os.path.exists(FRAMES_DIR_PATH):
            os.makedirs(FRAMES_DIR_PATH)
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
