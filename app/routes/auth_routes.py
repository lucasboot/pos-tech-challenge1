from flask import Blueprint, request, jsonify
from app.utils.auth import generate_token
from flasgger import swag_from

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'summary': 'Login do usuário',
    'description': 'Autentica um usuário e retorna um token JWT',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'example': 'admin'},
                    'password': {'type': 'string', 'example': 'password123'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login realizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string'},
                    'message': {'type': 'string'},
                    'expires_in': {'type': 'integer'}
                }
            }
        },
        401: {
            'description': 'Credenciais inválidas'
        }
    }
})
def login():
    """Endpoint de login para obter token JWT"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username e password são obrigatórios'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    # Validação simples (em produção, usar hash de senha e banco de dados)
    if username == 'admin' and password == 'password123':
        token = generate_token(user_id=username)
        return jsonify({
            'token': token,
            'message': 'Login realizado com sucesso',
            'expires_in': 3600
        }), 200
    
    return jsonify({'message': 'Credenciais inválidas'}), 401

@auth_bp.route('/auth/validate', methods=['GET'])
@swag_from({
    'tags': ['Autenticação'],
    'summary': 'Validar token',
    'description': 'Valida se o token JWT é válido',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token'
        }
    ],
    'responses': {
        200: {
            'description': 'Token válido',
            'schema': {
                'type': 'object',
                'properties': {
                    'valid': {'type': 'boolean'},
                    'user_id': {'type': 'string'}
                }
            }
        },
        401: {
            'description': 'Token inválido'
        }
    }
})
def validate_token():
    """Endpoint para validar token JWT"""
    from app.utils.auth import verify_token
    
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({'message': 'Token inválido'}), 401
    
    if not token:
        return jsonify({'message': 'Token é obrigatório'}), 401
    
    payload = verify_token(token)
    if payload:
        return jsonify({
            'valid': True,
            'user_id': payload.get('user_id')
        }), 200
    
    return jsonify({'valid': False, 'message': 'Token inválido'}), 401 