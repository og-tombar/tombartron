from OpenGL.GL import *


class Camera:
    def __init__(self):
        self.pos = {'x': 0.0, 'y': 0.0, 'z': 5.0}
        self.rot = {'yaw': 0.0, 'pitch': 45.0, 'roll': 0.0}

    # we use negative coords for position as glTranslatef moves the scene elements rather than the camera
    def update(self) -> None:
        glTranslatef(-self.pos['x'], -self.pos['y'], -self.pos['z'])
        glRotatef(self.rot['yaw'], 0, 1, 0)  # Yaw
        glRotatef(self.rot['pitch'], 1, 0, 0)  # Pitch
        glRotatef(self.rot['roll'], 0, 0, 1)  # Roll

    def set_position(self, new_x: float, new_y: float, new_z: float) -> None:
        self.pos['x'] = new_x
        self.pos['y'] = new_y
        self.pos['z'] = new_z

    def move(self, dx: float, dy: float, dz: float) -> None:
        self.set_position(self.pos['x'] + dx, self.pos['y'] + dy, self.pos['z'] + dz)

    def set_rotation(self, yaw: float, pitch: float, roll: float) -> None:
        self.rot['yaw'] = yaw
        self.rot['pitch'] = pitch
        self.rot['roll'] = roll

    def rotate(self, d_yaw: float, d_pitch: float, d_roll: float) -> None:
        self.set_rotation(self.rot['yaw'] + d_yaw, self.rot['pitch'] + d_pitch, self.rot['roll'] + d_roll)
