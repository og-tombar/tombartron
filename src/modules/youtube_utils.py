import json
import random
from enum import Enum

from modules.paths import *
from modules.youtube_api_controller import upload_video_to_youtube


class TitleType(Enum):
    NOUN_NOUN = 1
    NOUN_OF_NOUN = 2
    NOUN_AND_NOUN = 3
    NOUN_OR_NOUN = 4
    NOUN_NOT_NOUN = 5


def random_noun() -> str:
    with open(NOUN_LIST_JSON_PATH, 'r') as file:
        noun_list = json.load(file)
        return random.choice(noun_list)


def generate_video_title() -> str:
    with open(PROJECT_DATA_JSON_PATH, 'r') as file:
        j = json.load(file)
        video_count = j.get('video_count', 0) + 1

    with open(PROJECT_DATA_JSON_PATH, 'w') as file:
        j['video_count'] = video_count
        json.dump(j, file, indent=4, ensure_ascii=False)

    PREFIX = f"TOMBARtron Experiment no' {video_count}: "
    title_type = random.choice(list(TitleType)).name

    match title_type:
        case 'NOUN_NOUN':
            connector = ' '
        case 'NOUN_OF_NOUN':
            connector = ' Of '
        case 'NOUN_AND_NOUN':
            connector = ' And '
        case 'NOUN_OR_NOUN':
            connector = ' Or '
        case 'NOUN_NOT_NOUN':
            connector = ', Not '
        case _:
            connector = ' '

    return PREFIX + random_noun() + connector + random_noun()


def upload_video_with_default_config():
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
