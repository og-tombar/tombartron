import sys

from modules.all_utils import *


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # defaulting to hidden video render mode if no arguments provided
        scene = Scene(hidden=True)
        render_movie(scene)
        exit()

    scene = Scene()
    mode = sys.argv[1]
    match mode:
        case '-r':
            # render video mode
            render_movie(scene)
        case '-i':
            # interactive mode
            scene.play_scene()
        case _:
            # default
            print(f'Error: Invalid mode "{mode}".')
