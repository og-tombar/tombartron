import httplib2
import sys

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from modules.paths import *


def upload_video_to_youtube(video_path, title, description, tags=None, category_id=None):
    CLIENT_SECRETS_FILE = YOUTUBE_SECRET_PATH
    API_NAME = "youtube"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=SCOPES)
    storage = Storage(OAUTH_STORAGE_PATH)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flags = argparser.parse_args()
        credentials = run_flow(flow, storage, flags)

    youtube = build(API_NAME, API_VERSION, http=credentials.authorize(httplib2.Http()))

    try:
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": "public"
            }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print("Uploaded %d%%." % int(status.progress() * 100))

        print("Video upload completed!")

        video_id = response["id"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url

    except HttpError as e:
        print("An HTTP error occurred:")
        print(e)
        return None
