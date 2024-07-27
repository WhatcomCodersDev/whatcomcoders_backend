import json
import collections

collections.Iterable = collections.abc.Iterable

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services import firestore_db, sendgrid_wrapper

bp = Blueprint("profiles", __name__)

@bp.route("/profile/<slug>", methods=["GET"])
def get_profile_by_name(slug):
    user_data = firestore_db.get_profile_by_slug(slug)
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({"error": "User not found"}), 404
    
@bp.route("/profile/<slug>/email", methods=["GET"])
@jwt_required()
def send_email_to_user(slug):
    user_data = firestore_db.get_profile_by_slug(slug)
    print("user_data:", user_data)
    
    # current_user_uuid = get_jwt_identity()
    current_user_data = firestore_db.get_user_data_by_uuid("cda573aa-ac80-4f57-9a3c-aa71f13e9290")
    print("current_user_data:", current_user_data)
    if user_data:
        user_data["emailReachOutCount"] -= 1
        sendgrid_wrapper.send_email_intro(current_user_data, user_data)
        return jsonify({"message": "Email sent successfully"})
    else:
        return jsonify({"error": "User not found"}), 404