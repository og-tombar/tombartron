class Colors:
    rgb = {
        'black': (0.0, 0.0, 0.0),
        'white': (1.0, 1.0, 1.0),
        'dark_gray': (0.05, 0.05, 0.05),
        'red': (1.0, 0.0, 0.0),
        'green': (0.0, 1.0, 0.0),
        'blue': (0.0, 0.0, 1.0),
    }
    rgba = {
        'black': (0.0, 0.0, 0.0, 1),
        'dark_gray': (0.15, 0.15, 0.15, 1)
    }


class Gradient8:
    def __init__(self, colors: list[str] = None):
        colors = ['white', 'black'] * 4 if colors is None else colors
        match len(colors):
            case 2:
                self.colors = [colors[0], colors[1], colors[1], colors[0], colors[0], colors[1], colors[1], colors[0]]
            case 4:
                self.colors = [colors[0], colors[1], colors[2], colors[3], colors[1], colors[0], colors[3], colors[2]]
            case 8:
                self.colors = colors
            case _:
                self.colors = [colors[i % len(colors)] for i in range(8)]

    def get_cube_z_rotated(self, amount: int = 1) -> list[str]:
        # rotates cube colors clockwise
        new = self.colors
        for i in range(amount):
            old = new
            new = old.copy()
            # front face
            new[0], new[1], new[2], new[3] = old[1], old[2], old[3], old[0]
            # back face
            new[4], new[5], new[6], new[7] = old[7], old[4], old[5], old[6]
        return new

    def __repr__(self):
        return self.colors
