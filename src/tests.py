# from modules.all_utils import *

# import os

# from moviepy.editor import ImageSequenceClip, AudioFileClip

# def combine_frames_with_audio(frames_folder, audio_file, output_path):
#     frames = [f"{frames_folder}/{frame}" for frame in sorted(os.listdir(frames_folder))]
#     video_clip = ImageSequenceClip(frames, fps=60)
#     audio_clip = AudioFileClip(audio_file)
#     final_clip = video_clip.set_audio(audio_clip)
#     final_clip.write_videofile(output_path, codec='libx264')

# # Example usage
# frames_folder = FRAMES_DIR_PATH
# audio_file = OUTPUT_DIR_PATH + '/simple_chord.wav'
# output_path = OUTPUT_DIR_PATH + '/video.mp4'

# combine_frames_with_audio(frames_folder, audio_file, output_path)