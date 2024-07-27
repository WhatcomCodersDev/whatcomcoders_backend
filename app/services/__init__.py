from app.services.google_flow_manager import GoogleSignInFlowManager
from app.services.logger_manager import LoggerManager
from app.services.firestore_wrapper import FirestoreDBWrapper
from app.services.sendgrid_wrapper import SendGridWrapper
from google.cloud import firestore 
from flask_jwt_extended import JWTManager

jwt_manager = JWTManager()
firestore_client = firestore.Client()

google_signin_flow_manager = GoogleSignInFlowManager()
firestore_db = FirestoreDBWrapper(firestore_client)
logger_manager = LoggerManager()
sendgrid_wrapper = SendGridWrapper()