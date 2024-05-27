import json
import collections

collections.Iterable = collections.abc.Iterable

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.wrappers import Response
from flask.globals import request, session

from app.services import  jwt_manager, firestore_db, logger_manager

bp = Blueprint("user", __name__)

@bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({"message": "This is a protected route"})

@bp.route('/current_user', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)


@bp.route("/api/user/<slug>", methods=["GET"])
def get_user_data(slug):
    user_data = firestore_db.get_user_data_by_slug(slug)
    print(user_data)
    if user_data.exists:
        return jsonify(user_data.to_dict())
    else:
        return jsonify({"error": "User not found"}), 404
    
@bp.route("/api/people", methods=["GET"])
def get_all_users():
    print("calling /api/people endpoint")
    users_list = firestore_db.get_all_users()
    print("calling /api/people endpoint results:", jsonify(users_list))
    return jsonify(users_list)

@bp.route("/api/people/update", methods=["POST"])
def update_user_info():
    data = request.json
    firestore_db.update_user_info(data)
    return jsonify({"message": "User updated successfully"})

@bp.route("/api/current_user", methods=["GET"])
@jwt_required()
def current_user():
    try:
        current_user_uuid = get_jwt_identity()
        print("current_user_uuid", current_user_uuid)
        user_data = firestore_db.get_user_data_by_uuid(current_user_uuid) 
        print("user_data", user_data)
        user_data['uuid'] = current_user_uuid
        return jsonify(user_data)
    except Exception as e:
        print(f"Error getting current user: {e}")
        return jsonify({"error": "Error getting current user"}), 500

@bp.route("/api/user", methods=["GET"])
@jwt_required()
def get_user():
    current_user_uuid = get_jwt_identity()
    logger_manager.logger.debug("current_user_uuid", current_user_uuid)
    user_data = firestore_db.get_user_data_by_uuid(current_user_uuid) 
    user_data['uuid'] = current_user_uuid
    return jsonify(user_data)

@jwt_manager.invalid_token_loader
def invalid_token_callback(error):
    logger_manager.logger.error(f"Invalid token: {error}")
    return jsonify({
        'message': 'Invalid token.',
        'error': str(error)
    }), 422