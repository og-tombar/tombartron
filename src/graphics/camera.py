import math

from OpenGL.GLU import *


class Camera:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 5
        self.z_pos = 5

        self.yaw = 0
        self.pitch = 45
        self.roll = 0

        self.move_speed = 0.001
        self.rotation_speed = 0.01

        self.forward = self.calc_forward_vec()
        self.right = self.calc_right_vec()
        self.dt = 0

    def update(self, dt: float = 1) -> None:
        self.dt = dt
        self.forward = self.calc_forward_vec()
        self.right = self.calc_right_vec()

        forward_x = self.x_pos + self.forward[0]
        forward_y = self.y_pos + self.forward[1]
        forward_z = self.z_pos + self.forward[2]

        gluLookAt(self.x_pos, self.y_pos, self.z_pos, forward_x, forward_y, forward_z, 0, 1, 0)

    def set_position(self, x_pos: float, y_pos: float, z_pos: float) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos

    def move(self, dx: float, dy: float, dz: float) -> None:
        self.set_position(self.x_pos + dx * self.dt, self.y_pos + dy * self.dt, self.z_pos + dz * self.dt)

    def move_forward(self):
        dx = self.forward[0] * self.move_speed
        dy = self.forward[1] * self.move_speed
        dz = self.forward[2] * self.move_speed
        self.move(dx, dy, dz)

    def move_back(self):
        dx = -self.forward[0] * self.move_speed
        dy = -self.forward[1] * self.move_speed
        dz = -self.forward[2] * self.move_speed
        self.move(dx, dy, dz)

    def move_left(self):
        dx = -self.right[0] * self.move_speed
        dy = -self.right[1] * self.move_speed
        dz = -self.right[2] * self.move_speed
        self.move(dx, dy, dz)

    def move_right(self):
        dx = self.right[0] * self.move_speed
        dy = self.right[1] * self.move_speed
        dz = self.right[2] * self.move_speed
        self.move(dx, dy, dz)

    def move_up(self):
        dy = self.move_speed
        self.move(0, dy, 0)

    def move_down(self):
        dy = -self.move_speed
        self.move(0, dy, 0)

    def set_rotation(self, yaw: float, pitch: float, roll: float) -> None:
        self.yaw = (yaw + 180) % 360 - 180  # should be between (-179, 180), rotates on overflow / underflow
        self.pitch = max(min(pitch, 89), -89)  # should be in (-89, 89), doesn't rotate on overflow / underflow
        self.roll = roll

    def rotate(self, d_yaw: float, d_pitch: float, d_roll: float) -> None:
        self.set_rotation(self.yaw + d_yaw * self.dt, self.pitch + d_pitch * self.dt, self.roll + d_roll * self.dt)

    def calc_forward_vec(self) -> (float, float, float):
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)

        x = math.sin(yaw_rad) * math.cos(pitch_rad)
        y = -math.sin(pitch_rad)
        z = -math.cos(yaw_rad) * math.cos(pitch_rad)
        return x, y, z

    def calc_right_vec(self) -> (float, float, float):
        return -self.forward[2], 0, self.forward[0]
