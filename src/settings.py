import os

SECRET_KEY = os.environ.get("SECRET_KEY")
APP_ID = os.environ.get("APP_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
SCOPE = os.environ.get("SCOPE")
PORTAL_ID = os.environ.get("PORTAL_ID")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT", 27012))
MONGODB_SETTINGS = {"db": DB_NAME,
                    "host": DB_HOST,
                    "port": DB_PORT}
