from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from config.paths import *


def get_youtube_service():
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    creds = None

    if os.path.exists(CLIENT_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(CLIENT_TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(CLIENT_TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def upload_video_to_youtube(video_path, title, description, tags=None, category_id=None):
    service = get_youtube_service()

    try:
        body = {
            "snippet": {"title": title, "description": description, "tags": tags, "categoryId": category_id},
            "status": {"privacyStatus": "private"}
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = service.videos().insert(part=",".join(body.keys()), body=body, media_body=media)

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
