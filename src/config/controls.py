import numpy as np
import pygame
from pygame.locals import *

from graphics.camera import Camera


class Controls:
    def __init__(self, camera: Camera):
        self.camera = camera
        self.pressed = pygame.key.get_pressed()

    def handle_key_events(self) -> None:
        self.pressed = pygame.key.get_pressed()
        self.handle_camera_events()

    def handle_camera_events(self) -> None:
        # movement
        if self.pressed[K_w]:
            self.camera.move_forward()
        if self.pressed[K_s]:
            self.camera.move_back()
        if self.pressed[K_a]:
            self.camera.move_left()
        if self.pressed[K_d]:
            self.camera.move_right()
        if self.pressed[K_q]:
            self.camera.move_down()
        if self.pressed[K_e]:
            self.camera.move_up()

        # rotation
        if self.pressed[K_LEFT]:
            self.camera.rotate_left()
        if self.pressed[K_RIGHT]:
            self.camera.rotate_right()
        if self.pressed[K_UP]:
            self.camera.rotate_up()
        if self.pressed[K_DOWN]:
            self.camera.rotate_down()

    def should_pygame_quit(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
        return False
