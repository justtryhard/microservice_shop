from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
REDIS_URL = os.getenv("REDIS_URL")
ALGORITHM = os.getenv("ALGORITHM")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"