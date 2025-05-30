from flask import Blueprint, jsonify
from app.services.embrapa_service import EmbrapaService
from app.utils.pagination import get_pagination_params, paginate_data, get_filter_params
from app.utils.auth import optional_token
from flasgger import swag_from

processamento_bp = Blueprint('processamento', __name__)

@processamento_bp.route('/processamento', methods=['GET'])
@optional_token
@swag_from({
    'tags': ['Processamento'],
    'summary': 'Obter dados de processamento',
    'description': 'Retorna dados de processamento de uvas da Embrapa com suporte a paginação e filtros',
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'description': 'Número da página (padrão: 1)'
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'description': 'Itens por página (padrão: 50, máximo: 1000)'
        },
        {
            'name': 'ano',
            'in': 'query',
            'type': 'integer',
            'description': 'Filtrar por ano'
        },
        {
            'name': 'cultivar',
            'in': 'query',
            'type': 'string',
            'description': 'Filtrar por cultivar'
        },
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'description': 'Bearer token (opcional)'
        }
    ],
    'responses': {
        200: {
            'description': 'Dados de processamento retornados com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'ano': {'type': 'integer'},
                                'cultivar': {'type': 'string'},
                                'quantidade': {'type': 'integer'},
                                'unidade': {'type': 'string'}
                            }
                        }
                    },
                    'pagination': {
                        'type': 'object',
                        'properties': {
                            'page': {'type': 'integer'},
                            'per_page': {'type': 'integer'},
                            'total': {'type': 'integer'},
                            'pages': {'type': 'integer'},
                            'has_prev': {'type': 'boolean'},
                            'has_next': {'type': 'boolean'}
                        }
                    }
                }
            }
        },
        500: {
            'description': 'Erro interno do servidor'
        }
    }
})
def get_processamento():
    """Endpoint para obter dados de processamento"""
    try:
        service = EmbrapaService()
        page, per_page = get_pagination_params()
        filters = get_filter_params()
        
        data = service.get_data('processamento')
        
        if filters.get('ano'):
            data = [item for item in data if item.get('ano') == filters['ano']]
        
        if filters.get('cultivar'):
            data = [item for item in data if filters['cultivar'].lower() in item.get('cultivar', '').lower()]
        
        result = paginate_data(data, page, per_page)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor', 'message': str(e)}), 500

@processamento_bp.route('/processamento/anos', methods=['GET'])
@optional_token
@swag_from({
    'tags': ['Processamento'],
    'summary': 'Obter anos disponíveis',
    'description': 'Retorna lista de anos disponíveis nos dados de processamento',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'description': 'Bearer token (opcional)'
        }
    ],
    'responses': {
        200: {
            'description': 'Anos disponíveis',
            'schema': {
                'type': 'object',
                'properties': {
                    'anos': {
                        'type': 'array',
                        'items': {'type': 'integer'}
                    }
                }
            }
        }
    }
})
def get_processamento_anos():
    """Endpoint para obter anos disponíveis nos dados de processamento"""
    try:
        service = EmbrapaService()
        data = service.get_data('processamento')
        
        anos = sorted(list(set(item.get('ano') for item in data if item.get('ano'))))
        
        return jsonify({'anos': anos}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor', 'message': str(e)}), 500

@processamento_bp.route('/processamento/cultivares', methods=['GET'])
@optional_token
@swag_from({
    'tags': ['Processamento'],
    'summary': 'Obter cultivares disponíveis',
    'description': 'Retorna lista de cultivares disponíveis nos dados de processamento',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'description': 'Bearer token (opcional)'
        }
    ],
    'responses': {
        200: {
            'description': 'Cultivares disponíveis',
            'schema': {
                'type': 'object',
                'properties': {
                    'cultivares': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_processamento_cultivares():
    """Endpoint para obter cultivares disponíveis nos dados de processamento"""
    try:
        service = EmbrapaService()
        data = service.get_data('processamento')
        
        cultivares = sorted(list(set(item.get('cultivar') for item in data if item.get('cultivar'))))
        
        return jsonify({'cultivares': cultivares}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor', 'message': str(e)}), 500 