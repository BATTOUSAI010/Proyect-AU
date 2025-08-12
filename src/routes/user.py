from flask import Blueprint, jsonify, request
from ..models.user import User, db

user_bp = Blueprint('user', __name__)


@user_bp.route('/users', methods=['GET'])
def list_users():
    """Return all users."""
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user with name and email provided in JSON."""
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({'error': 'name and email are required'}), 400

    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201
