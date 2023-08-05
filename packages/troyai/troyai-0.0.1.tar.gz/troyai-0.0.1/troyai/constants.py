import string

DEFAULT_HOST = "http://127.0.0.1:3000"
CREATE_AUTO_PATH = "/ai_models/create_auto"

TOKEN_LENGTH = 16
BASE62 = string.ascii_letters + string.digits

NAME_MIN_LENGTH = 3
NAME_MAX_LENGTH = 30

DESCRIPTION_MIN_LENGTH = 5
DESCRIPTION_MAX_LENGTH = 400