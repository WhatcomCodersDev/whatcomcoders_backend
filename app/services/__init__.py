from app.services.flow_manager import FlowManager
from app.services.logger_manager import LoggerManager
from app.services.firestore_wrapper import FirestoreDBWrapper
from app.services.sendgrid_wrapper import SendGridWrapper
from app.utils import setup_google_auth_flow
from google.cloud import firestore 
from flask_jwt_extended import JWTManager

jwt_manager = JWTManager()
firestore_client = firestore.Client()
flow = setup_google_auth_flow()

flow_manager = FlowManager(flow)
firestore_db = FirestoreDBWrapper(firestore_client)
logger_manager = LoggerManager()
sendgrid_wrapper = SendGridWrapper()