import sys

from graphics.scene import Scene
from video.video_utils import render_video
from youtube.youtube_utils import upload_video_with_default_config


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # defaulting to hidden video render mode if no arguments provided
        scene = Scene(hidden=True)
        render_video(scene)
        upload_video_with_default_config()

    elif sys.argv[1] == '-w':
        # windowed interactive mode
        scene = Scene()
        scene.play_scene()

    elif sys.argv[1] == '-fs':
        # fullscreen interactive mode
        scene = Scene(fullscreen=True)
        scene.play_scene()

    elif sys.argv[1] == '-r':
        # render video mode
        scene = Scene()
        render_video(scene)

    else:
        # default
        print(f'Error: Invalid mode "{sys.argv[1]}".')
