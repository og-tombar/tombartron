from moviepy.editor import ImageSequenceClip, AudioFileClip

from music.audio_utils import *
from config.paths import *
from config.other_utils import *


def combine_frames_and_audio(frames_dir, audio_file, output_path) -> None:
    frames = [f"{frames_dir}/{frame}" for frame in sorted(os.listdir(frames_dir))]
    video_clip = ImageSequenceClip(frames, fps=60)
    audio_clip = AudioFileClip(audio_file)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')


def render_movie(scene, render_time=2.0) -> None:
    scene.render_movie_frames(render_time)
    simple_chord()
    combine_frames_and_audio(FRAMES_DIR_PATH, OUTPUT_DIR_PATH + '/simple_chord.wav', OUTPUT_DIR_PATH + '/video.mp4')
    empty_dir(FRAMES_DIR_PATH)
