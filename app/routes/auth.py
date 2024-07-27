import json
import collections
import uuid

collections.Iterable = collections.abc.Iterable

import datetime

from flask import Blueprint, make_response, redirect, current_app, request
from flask_jwt_extended import create_access_token
from flask.wrappers import Response

from app.utils import upload_photo_to_bucket
from app.services import google_signin_flow_manager, firestore_db


bp = Blueprint("auth", __name__)

@bp.route("/auth/google")
def login():
    '''Login function for Google OAuth2.0.
    
    After getting the authorization URL, redirect to the callback function below 
    with the auth
    '''
    try:
        authorization_url, state = google_signin_flow_manager.get_flow_authorization_url()
        return Response(response=json.dumps({'auth_url': authorization_url}),
                        status=200,
                        mimetype='application/json')
    except Exception as e:
        print(f"Error during Google OAuth login: {str(e)}")
        return Response(response=json.dumps({'error': 'Failed to get authorization URL'}),
                        status=500,
                        mimetype='application/json')


@bp.route("/callback")
def callback():
    '''Callback function used for signing in with Google OAuth2.0.
    
    1. Get the credentials and info from the flow manager 
    2. Search up user's collection in firebase using their email
    3. If the user doesn't exist, create a new user in the database
    4. Create an access token for the user  and redirect the user to the people page
    
    '''
    try:
        authorization_response_url = request.url
        credentials = google_signin_flow_manager.get_credentials_from_flow(authorization_response_url)
        
        id_info = google_signin_flow_manager.get_id_info(credentials)
        user_info = google_signin_flow_manager.get_user_info(credentials)
    except Exception as e:
        print(f"Error during OAuth callback: {str(e)}")
        return Response(response=json.dumps({'error': 'OAuth callback failed'}),
                        status=500,
                        mimetype='application/json')

    try:
        user_doc = firestore_db.get_user_doc_by_email(user_info.get("email"))
        if not user_doc:
            user_uuid = str(uuid.uuid4())
            access_token = create_access_token(identity=user_uuid, expires_delta=datetime.timedelta(hours=2))
            user_slug = generate_user_slug(user_info.get("name"), user_uuid)
            user_info["user_slug"] = user_slug
            user_info["completed_profile"] = False
            user_info["emailReachOutCount"] = 3
            if user_info.get("picture"):
                upload_photo_to_bucket(user_info.get("picture"), id_info.get("sub"))
            firestore_db.store_user_in_db(user_info, user_uuid)
            redirect_url = f'{current_app.config["BASE_URL"]}/signup'
        else:
            access_token = create_access_token(identity=user_doc.id, expires_delta=datetime.timedelta(hours=2))
            redirect_url = f'{current_app.config["BASE_URL"]}/people'
    except Exception as e:
        print(f"Error during user processing: {str(e)}")
        return Response(response=json.dumps({'error': 'User processing failed'}),
                        status=500,
                        mimetype='application/json')

    response = make_response(redirect(redirect_url))
    set_access_token_cookie(response, access_token)
    return response

def generate_user_slug(name, user_uuid):
    '''Generate a user slug based on the user's name and UUID.'''
    return name.replace(" ", "-").lower() + "-" + str(user_uuid)[-6:]

def set_access_token_cookie(response, access_token):
    '''Set the access token cookie in the response.'''
    response.set_cookie('access_token_cookie', 
                        access_token, 
                        httponly=True, 
                        samesite=current_app.config["SAMESITE_COOKIE_SETTING"], 
                        secure=current_app.config.get("SECURE_COOKIES", False), 
                        path='/',
                        max_age=60*60*2) # Cookie expires in 2 hours



@bp.route("/auth/logout", methods=["POST"])
def logout():
    response = make_response()
    # Clear the access_token_cookie
    response.set_cookie('access_token_cookie', '', expires=0)
    return response