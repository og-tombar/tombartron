import os

# main directories
MODULES_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(MODULES_PATH)
OUTPUT_DIR_PATH = ROOT_PATH + '/output'
FRAMES_DIR_PATH = OUTPUT_DIR_PATH + '/frames'

# soundfonts
SOUNDFONTS_DIR_PATH = ROOT_PATH + '/soundfonts'
YAMAHA_C7_SF2_PATH = SOUNDFONTS_DIR_PATH + '/Yamaha_C7__Normalized_.sf2'
CTK_533_SF2_PATH = SOUNDFONTS_DIR_PATH + '/CTK-533_Piano1__00___Casio_.sf2'

# resources
RESOURCES_PATH = ROOT_PATH + '/resources'
PROJECT_DATA_JSON_PATH = RESOURCES_PATH + '/project_data.json'
NOUN_LIST_JSON_PATH = RESOURCES_PATH + '/noun_list.json'
SCENE_ELEMENTS_JSON_PATH = RESOURCES_PATH + '/scene_elements.json'

# credentials
CREDENTIALS_DIR_PATH = os.path.dirname(os.path.dirname(ROOT_PATH)) + '/credentials'
CLIENT_SECRET_PATH = CREDENTIALS_DIR_PATH + '/client_secret.json'
CLIENT_TOKEN_PATH = CREDENTIALS_DIR_PATH + '/token.json'
