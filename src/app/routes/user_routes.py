from flask import Blueprint, jsonify
from app.services.user_service import UserService
from app.metrics import track_exceptions

user_blueprint = Blueprint('user_blueprint', __name__)
user_service = UserService()

@user_blueprint.route('/users', methods=['GET'])
@track_exceptions
def get_users():
    users = user_service.get_users()
    return jsonify(users), 200

@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
@track_exceptions
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404

@user_blueprint.route('/users/<int:user_id>/error', methods=['GET'])
@track_exceptions
def simulate_user_error(user_id):
    """Endpoint that demonstrates exception handling"""
    if user_id == 999:
        raise ValueError("Invalid user data provided")
    elif error_type == "runtime":
        raise RuntimeError("User service temporarily unavailable")
    else:
        return jsonify({"message": f"User {user_id} processed successfully"}), 200
