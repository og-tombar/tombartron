import os

# main directories
MODULES_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(MODULES_PATH)
OUTPUT_DIR_PATH = ROOT_PATH + '/output'
FRAMES_DIR_PATH = OUTPUT_DIR_PATH + '/frames'

# soundfonts
SOUNDFONTS_DIR_PATH = ROOT_PATH + '/soundfonts'
YAMAHA_C7_SF2_PATH = SOUNDFONTS_DIR_PATH + '/piano_yamaha_c7.sf2'
CTK_533_SF2_PATH = SOUNDFONTS_DIR_PATH + '/piano_casio_ctk533.sf2'

# youtube
YOUTUBE_DIR_PATH = ROOT_PATH + '/youtube'
NOUN_LIST_JSON_PATH = YOUTUBE_DIR_PATH + '/noun_list.json'
PROJECT_DATA_JSON_PATH = YOUTUBE_DIR_PATH + '/project_data.json'

# credentials - paths are not in this repo for security purposes
CREDENTIALS_DIR_PATH = os.path.dirname(os.path.dirname(ROOT_PATH)) + '/credentials'
CLIENT_SECRET_PATH = CREDENTIALS_DIR_PATH + '/client_secret.json'
CLIENT_TOKEN_PATH = CREDENTIALS_DIR_PATH + '/token.json'
