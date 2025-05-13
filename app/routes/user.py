from flask import jsonify, request, Blueprint
from app.models import User
from app.app import mysql  # ou `db` se estiver usando SQLAlchemy diretamente
from app.routes import bp
from app.routes.auth import token_required

# Obter todos os usuários ou um específico
@bp.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    user_id = request.args.get('user_id')
    if user_id:
        try:
            user = User.query.get_or_404(user_id)
            return jsonify(user.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        try:
            users = User.query.all()
            return jsonify([user.to_dict() for user in users]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


# Criar novo usuário
@bp.route('/users', methods=['POST'])
@token_required
def create_user(current_user):
    try:
        data = request.get_json()
        if 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and email are required'}), 400

        if User.query.filter_by(name=data['name']).first():
            return jsonify({'error': 'Name already registered'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400

        user = User(name=data['name'], email=data['email'])
        mysql.session.add(user)
        mysql.session.commit()
        return jsonify(user.to_dict()), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Atualizar usuário
@bp.route('/users/<int:id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
    try:
        user = User.query.get_or_404(id)
        data = request.get_json() or {}

        if 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and email are required'}), 400

        # Evitar conflitos com outros usuários
        if User.query.filter(User.name == data['name'], User.id != id).first():
            return jsonify({'error': 'Name already registered'}), 400
        if User.query.filter(User.email == data['email'], User.id != id).first():
            return jsonify({'error': 'Email already registered'}), 400

        user.name = data['name']
        user.email = data['email']
        mysql.session.commit()
        return jsonify(user.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Deletar usuário
@bp.route('/users/<int:id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    try:
        user = User.query.get_or_404(id)
        mysql.session.delete(user)
        mysql.session.commit()
        return jsonify({'message': 'Successfully deleted user'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
