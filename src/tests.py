from modules.all_utils import *


def test_video_upload():
    video_path = OUTPUT_DIR_PATH + '/video.mp4'
    title = generate_video_title()
    description = "This video is an early TOMBARtron experiment." \
                  "Experiments will progressively improve in results with every iteration."
    tags = ["Music", "Programming", "Python", "OpenGL", "Generative", "Experiment"]
    category_id = "10"

    video_url = upload_video_to_youtube(video_path, title, description, tags, category_id)
    if video_url:
        print("Video uploaded successfully!")
        print("YouTube URL:", video_url)
    else:
        print("Video upload failed.")


test_video_upload()
