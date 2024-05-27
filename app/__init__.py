from flask import Flask
from flask_cors import CORS
from config import *
from app.routes import auth, user, user_profile, directory
from app.handlers import errors
from app.services import firestore_db, flow_manager, jwt_manager, logger_manager, sendgrid_wrapper
from dotenv import load_dotenv


def create_flask_app() -> Flask:
    load_dotenv()
    environment = os.environ.get('FLASK_ENV')
    if environment == 'production':
        dotenv_path = '.env.prod'
    elif environment == 'staging':
        dotenv_path = '.env.staging'
    else:
        dotenv_path = '.env'  # Default to the main .env for development

    load_dotenv(dotenv_path=dotenv_path)

    app = Flask(__name__)
    
    if environment == 'development':
        app.config.from_object('config.DevelopmentConfig')
        allowed_origins = [
            "http://127.0.0.1:4000",
            "http://127.0.0.1:3000",
            "http://localhost:3000", 
            "http://localhost:4000",
            "http://localhost:8080",
        ]
    elif environment == 'staging':
        app.config.from_object('config.StagingConfig')
        allowed_origins = [
            "https://staging.whatcomcoders.com",
            "https://staging.whatcomcoders.com",
        ]

    elif environment == 'production':
        app.config.from_object('config.ProductionConfig')
        allowed_origins = [
            # "https://gothic-sled-375305.uc.r.appspot.com"
            # "https://gothic-sled-375305.firebaseapp.com",
            # "https://gothic-sled-375305.web.app",
            "https://www.whatcomcoders.com",
            "https://whatcomcoders.com",
        ]

    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(user_profile.bp)
    app.register_blueprint(directory.bp)

    errors.register_error_handlers(app)

    app.secret_key = SECRET_KEY
    CORS(app, resources={r"/*": {
        "origins": allowed_origins,
        "supports_credentials": True}}, supports_credentials=True)

    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    
    print(JWT_SECRET_KEY)
    app.config["JWT_TOKEN_LOCATION"] = JWT_TOKEN_LOCATION
    print(JWT_TOKEN_LOCATION)
    
    jwt_manager.init_app(app)

    return app

app = create_flask_app()