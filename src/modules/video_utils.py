from moviepy.editor import ImageSequenceClip, AudioFileClip

from modules.pygame_config import *
from modules.audio_utils import *
from modules.paths import *
from modules.other_utils import *


def combine_frames_with_audio(frames_folder, audio_file, output_path) -> None:
    frames = [f"{frames_folder}/{frame}" for frame in sorted(os.listdir(frames_folder))]
    video_clip = ImageSequenceClip(frames, fps=60)
    audio_clip = AudioFileClip(audio_file)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')


def render_movie(render_time=2) -> None:
    render_movie_frames(render_time)
    simple_chord()
    combine_frames_with_audio(FRAMES_DIR_PATH, OUTPUT_DIR_PATH + '/simple_chord.wav', OUTPUT_DIR_PATH + '/video.mp4')
    empty_dir(FRAMES_DIR_PATH)
