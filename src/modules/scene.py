from time import time

import pygame
from pygame.locals import *
from OpenGL.GLU import *

from modules.paths import *
from graphics.geometries import *
from graphics.camera import Camera
from graphics.light import Light
from graphics.colors import Colors
from modules.scene_elements import SceneElements
from config.controls import Controls


class Scene:
    def __init__(self, hidden=False):
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600

        pygame.init()

        if hidden:
            pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), HIDDEN | DOUBLEBUF | OPENGL)
        else:
            pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
            # full screen:
            # pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.OPENGL)

        self.init_gl()
        self.light = Light()
        self.camera = Camera()
        self.controls = Controls(self.camera)
        self.scene_elements = SceneElements()
        self.dt = 0

    def init_gl(self) -> None:
        glClearColor(*Colors.rgba['dark_gray'])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # TODO: Change this to address full screen as well?
        gluPerspective(45, (self.WINDOW_WIDTH / self.WINDOW_HEIGHT), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def play_scene(self) -> None:
        clock = pygame.time.Clock()
        should_quit = False
        while not should_quit:
            self.dt = clock.tick(60)
            self.update_scene()
            should_quit = self.controls.should_pygame_quit()
        pygame.quit()
        print("Rendering complete.")

    def update_scene(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.controls.handle_key_events()
        self.camera.update(dt=self.dt)
        self.light.activate()
        self.scene_elements.render()
        self.light.deactivate()

        pygame.display.flip()
        glFlush()

    def render_frame_to_file(self, frame_count: int) -> None:
        pixels = glReadPixels(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, GL_RGB, GL_UNSIGNED_BYTE)
        surface = pygame.image.fromstring(pixels, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT), 'RGB')
        if not os.path.exists(FRAMES_DIR_PATH):
            os.makedirs(FRAMES_DIR_PATH)
        pygame.image.save(surface, f"{FRAMES_DIR_PATH}/frame_{frame_count:04d}.png")

    def render_movie_frames(self, render_time: float) -> None:
        start_time = time()
        elapsed_time = 0.0
        frame_count = 0
        quit_trigger = False

        while elapsed_time < render_time and not quit_trigger:
            self.update_scene()
            self.render_frame_to_file(frame_count)
            frame_count += 1
            elapsed_time = time() - start_time
            quit_trigger = self.controls.should_pygame_quit()

        pygame.quit()
        print(f"Saved {frame_count} frames as separate files.")
