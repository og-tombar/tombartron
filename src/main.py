import sys

from modules.all_utils import *


if __name__ == '__main__':
    init_scene()

    # defaulting to render mode
    if len(sys.argv) == 1:
        render_movie()
        exit()

    mode = sys.argv[1]
    match mode:
        case 'render':
            render_movie()
        case 'interactive':
            play_scene()
        case _:
            print(f'Error: Invalid mode "{mode}".')
