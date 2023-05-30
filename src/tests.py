from modules.paths import *
from youtube_api_backend import upload_video_to_youtube

# Example usage:
video_path = OUTPUT_DIR_PATH + '/video.mp4'
title = "My Awesome Video"
description = "Check out this amazing video I made!"
tags = ["video", "awesome"]
category_id = "22"  # Specify the category ID (e.g., "22" for Entertainment)

video_url = upload_video_to_youtube(video_path, title, description, tags, category_id)
if video_url:
    print("Video uploaded successfully!")
    print("YouTube URL:", video_url)
else:
    print("Video upload failed.")

