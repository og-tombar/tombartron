from OpenGL.GL import *


class Camera:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 2
        self.z_pos = 2
        self.yaw = 0
        self.pitch = 45
        self.roll = 0.0

    # we use negative coords for position as glTranslatef moves the scene elements rather than the camera
    def update(self) -> None:
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.roll, 0, 0, 1)
        glTranslatef(-self.x_pos, -self.y_pos, -self.z_pos)

    def set_position(self, x_pos: float, y_pos: float, z_pos: float) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos

    def move(self, dx: float, dy: float, dz: float) -> None:
        self.set_position(self.x_pos + dx, self.y_pos + dy, self.z_pos + dz)

    def set_rotation(self, yaw: float, pitch: float, roll: float) -> None:
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

    def rotate(self, d_yaw: float, d_pitch: float, d_roll: float) -> None:
        self.set_rotation(self.yaw + d_yaw, self.pitch + d_pitch, self.roll + d_roll)
