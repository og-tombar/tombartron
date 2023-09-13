import time

import pygame
from pygame.locals import *
from OpenGL.GLU import *

from modules.paths import *
from modules.geometries import *
from modules.camera import Camera
from modules.light import Light
from modules.colors import colors_rgba
from modules.scene_elements import SceneElements


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
        self.camera = Camera()
        self.light = Light()
        self.scene_elements = SceneElements()

    def init_gl(self) -> None:
        glClearColor(*colors_rgba['dark_gray'])
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

        self.process_pressed_keys()
        self.camera.update()
        self.light.activate()
        self.scene_elements.render()
        self.light.deactivate()

        pygame.display.flip()
        glFlush()

    # TODO: Create a pygame config class and move this function to it?
    def process_pressed_keys(self):
        keys = pygame.key.get_pressed()

        dx, dy, dz = 0, 0, 0
        d_yaw, d_pitch, d_roll = 0, 0, 0

        if keys[K_w]:
            self.camera.move_forward()
        if keys[K_s]:
            self.camera.move_back()
        if keys[K_a]:
            self.camera.move_left()
        if keys[K_d]:
            self.camera.move_right()
        if keys[K_q]:
            self.camera.move_up()
        if keys[K_e]:
            self.camera.move_down()

        if keys[K_LEFT]:
            d_yaw = -self.camera.rotation_speed
        if keys[K_RIGHT]:
            d_yaw = self.camera.rotation_speed
        if keys[K_UP]:
            d_pitch = -self.camera.rotation_speed
        if keys[K_DOWN]:
            d_pitch = self.camera.rotation_speed

        self.camera.move(dx, dy, dz)
        self.camera.rotate(d_yaw, d_pitch, d_roll)

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
