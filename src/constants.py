import os
from dotenv import load_dotenv

load_dotenv()


ALLOWED_ORIGIN = os.getenv("ALLOWED_HOSTS").split(",")
