import os 
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", 'secret') #fix
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", 'secret') #fix
GOOGLE_APPLICATION_CREDENTIALS = "gcloud_secrets.json"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
SESSION_COOKIE_SECURE = False
JWT_COOKIE_CSRF_PROTECT = True
JWT_TOKEN_LOCATION = ["cookies"]
CORS_ALLOW_ORIGIN = "*"
CORS_ALLOW_HEADERS = "Content-Type"
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
TEST_RECEIVER_EMAIL = os.getenv('TEST_RECEIVER_EMAIL')


class Config(object):
    DEBUG = False
    TESTING = False
 
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    HOST = "0.0.0.0"
    PORT = 4000
    REDIRECT_URI = "http://localhost:4000/callback" 
    BASE_URL = "http://localhost:3000"
    DOMAIN = "localhost"
    SAMESITE_COOKIE_SETTING = "Lax"
    BUCKET_NAME = os.getenv('BUCKET_NAME')


class StagingConfig(Config):
    HOST = "0.0.0.0"
    PORT = 8080
    REDIRECT_URI = "https://whatcomcoders-prod.web.app/callback" 
    BASE_URL = "https://whatcomcoders-prod.web.app/"
    DOMAIN = ".whatcomcoders-prod.web.app"
    SAMESITE_COOKIE_SETTING = "None"
    DEBUG = False
    BUCKET_NAME = os.getenv('BUCKET_NAME')


class ProductionConfig(Config):
    HOST = "0.0.0.0"
    PORT = 8080
    REDIRECT_URI = "https://www.whatcomcoders.com/callback" 
    BASE_URL = "https://www.whatcomcoders.com"
    DOMAIN = ".whatcomcoders.com"
    SAMESITE_COOKIE_SETTING = "None"
    DEBUG = False
    BUCKET_NAME = os.getenv('BUCKET_NAME')

