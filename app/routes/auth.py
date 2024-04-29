import json
import collections
import uuid

collections.Iterable = collections.abc.Iterable

from flask import Blueprint, make_response, redirect, current_app
from flask_jwt_extended import create_access_token
from flask.wrappers import Response

from app.utils import upload_photo_to_bucket
from app.services import flow_manager, firestore_db


bp = Blueprint("auth", __name__)

@bp.route("/callback")
def callback():
    print("current_app.config", current_app.config)
    credentials = flow_manager.get_credentials_from_flow()
    id_info = flow_manager.get_id_info(credentials)
    user_info = flow_manager.get_user_info(credentials)
    user_doc = firestore_db.get_user_doc_by_email(user_info.get("email"))
    
    if not user_doc:
        user_uuid = str(uuid.uuid4())
        access_token = create_access_token(identity=user_uuid)

        user_slug = user_info.get("name").replace(" ", "-").lower() + "-" + str(user_uuid)[-6:]
        user_info["user_slug"] = user_slug
        user_info["completed_profile"] = False
        user_info["emailReachOutCount"] = 3
        if user_info.get("picture"):
            upload_photo_to_bucket(user_info.get("picture"), id_info.get("sub"))
        firestore_db.store_user_in_db(user_info, user_uuid)
        redirect_url = f'{current_app.config["BASE_URL"]}/signup'
    else:
        access_token = create_access_token(identity=user_doc.id)
        redirect_url = f'{current_app.config["BASE_URL"]}/people'

    response = make_response(redirect(redirect_url))
    response.set_cookie('access_token_cookie', 
                        access_token, 
                        httponly=False, 
                        samesite=current_app.config["SAMESITE_COOKIE_SETTING"], 
                        # secure=True, enable during prod
                        # domain=".whatcomcoders.com", 
                        path='/')
    print(response)

    return response

@bp.route("/auth/google")
def login():
    authorization_url, state = flow_manager.get_flow_authorization_url()
    return Response(response=json.dumps({'auth_url': authorization_url}),
                    status=200,
                    mimetype='application/json')

@bp.route("/auth/logout", methods=["POST"])
def logout():
    response = make_response()
    # Clear the access_token_cookie
    response.set_cookie('access_token_cookie', '', expires=0)
    return response