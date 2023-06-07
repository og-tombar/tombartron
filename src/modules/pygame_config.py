import time
from pygame.locals import *

from modules.paths import *
from modules.opengl_config import *
from modules.opengl_shapes import *


def init_scene(hidden=False) -> None:
    pygame.init()
    if hidden:
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HIDDEN | DOUBLEBUF | OPENGL)
    else:
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
    init_gl()


def check_for_pygame_quit() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
    return False


def render_frame_to_file(frame_count) -> None:
    pixels = glReadPixels(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, GL_RGB, GL_UNSIGNED_BYTE)
    surface = pygame.image.fromstring(pixels, (WINDOW_WIDTH, WINDOW_HEIGHT), 'RGB')
    pygame.image.save(surface, f"{FRAMES_DIR_PATH}/frame_{frame_count:04d}.png")


def render_movie_frames(render_time) -> None:
    start_time = time.time()
    elapsed_time = 0.0
    frame_count = 0
    quit_trigger = False

    while elapsed_time < render_time and not quit_trigger:
        update_scene()
        render_frame_to_file(frame_count)
        frame_count += 1
        elapsed_time = time.time() - start_time
        quit_trigger = check_for_pygame_quit()

    pygame.quit()
    print(f"Saved {frame_count} frames as separate files.")


def play_scene():
    quit_trigger = False
    while not quit_trigger:
        update_scene()
        pygame.time.delay(int(1000 / 60))
        quit_trigger = check_for_pygame_quit()

    pygame.quit()
    print("Rendering complete.")
