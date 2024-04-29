from flask import jsonify
from flask_jwt_extended.exceptions import NoAuthorizationError
from app.services import logger_manager

def register_error_handlers(app):
    @app.errorhandler(NoAuthorizationError)
    def handle_auth_error(e):
        return jsonify({'message': str(e)}), 401

    @app.errorhandler(Exception)
    def handle_uncaught_exception(e):
        logger_manager.logger.error(f"Uncaught exception: {e}")
        return jsonify({
            'message': 'An unexpected error occurred.',
        }), 500
    @app.errorhandler(401)
    def custom_401(error):
        print("Unauthorized: " + str(error))
        logger_manager.logger.error(f"Unauthorized: {error}")
        return jsonify(message="Unauthorized: " + str(error)), 401