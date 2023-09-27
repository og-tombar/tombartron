import math

import numpy as np
from OpenGL.GLU import *


class Camera:
    def __init__(self, move_speed: float = 0.01, rot_speed: float = 0.1, pos: np.ndarray | list[float] = None,
                 rot: np.ndarray | list[float] = None):
        self.move_speed = move_speed
        self.rot_speed = rot_speed
        self.pos = np.array([0.0, 5.0, 5.0]) if pos is None else pos
        self.rot = np.array([0.0, 45.0, 0.0]) if rot is None else rot

        # position vectors
        self.up = np.array([0.0, 1.0, 0.0])
        self.relative_forward = self.calc_relative_forward_vec()
        self.relative_right = self.calc_relative_right_vec()

        # rotation vectors
        self.up_rot = np.array([0.0, -1.0, 0.0])
        self.right_rot = np.array([1.0, 0.0, 0.0])

        self.dt = 0.0

    def update(self, dt: float = 1) -> None:
        self.dt = dt
        gluLookAt(*self.pos, *(self.pos + self.relative_forward), 0, 1, 0)

    def set_position(self, pos: np.ndarray | list[float]) -> None:
        self.pos = pos

    def move(self, d_pos: np.ndarray | list[float]) -> None:
        self.set_position(self.pos + np.array(d_pos) * self.move_speed * self.dt)

    def move_forward(self) -> None:
        self.move(self.relative_forward)

    def move_back(self) -> None:
        self.move(-self.relative_forward)

    def move_left(self) -> None:
        self.move(-self.relative_right)

    def move_right(self) -> None:
        self.move(self.relative_right)

    def move_up(self) -> None:
        self.move(self.up)

    def move_down(self) -> None:
        self.move(-self.up)

    def set_rotation(self, rot: np.ndarray | list[float]) -> None:
        yaw = (rot[0] + 180) % 360 - 180  # should be between (-179, 180), rotates on overflow / underflow
        pitch = max(min(rot[1], 89), -89)  # should be in (-89, 89), doesn't rotate on overflow / underflow
        self.rot = np.array([yaw, pitch, rot[2]])
        self.relative_forward = self.calc_relative_forward_vec()
        self.relative_right = self.calc_relative_right_vec()

    def rotate(self, dr: np.ndarray | list[float]) -> None:
        self.set_rotation(self.rot + dr * self.rot_speed * self.dt)

    def rotate_left(self) -> None:
        self.rotate(-self.right_rot)

    def rotate_right(self) -> None:
        self.rotate(self.right_rot)

    def rotate_up(self) -> None:
        self.rotate(self.up_rot)

    def rotate_down(self) -> None:
        self.rotate(-self.up_rot)

    def calc_relative_forward_vec(self) -> np.ndarray:
        yaw_rad = math.radians(self.rot[0])
        pitch_rad = math.radians(self.rot[1])

        x = math.sin(yaw_rad) * math.cos(pitch_rad)
        y = -math.sin(pitch_rad)
        z = -math.cos(yaw_rad) * math.cos(pitch_rad)
        return np.array([x, y, z])

    def calc_relative_right_vec(self) -> np.ndarray:
        return np.array([-self.relative_forward[2], 0, self.relative_forward[0]])
