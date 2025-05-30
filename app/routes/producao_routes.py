from flask import Blueprint, jsonify
from app.services.embrapa_service import EmbrapaService
from app.utils.pagination import get_pagination_params, paginate_data, get_filter_params
from app.utils.auth import optional_token
from flasgger import swag_from

producao_bp = Blueprint('producao', __name__)

@producao_bp.route('/producao', methods=['GET'])
@optional_token
@swag_from({
    'tags': ['Produção'],
    'summary': 'Obter dados de produção',
    'description': 'Retorna dados de produção de vinhos da Embrapa com suporte a paginação e filtros',
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
            'name': 'produto',
            'in': 'query',
            'type': 'string',
            'description': 'Filtrar por produto'
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
            'description': 'Dados de produção retornados com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'ano': {'type': 'integer'},
                                'produto': {'type': 'string'},
                                'quantidade': {'type': 'integer'},
                                'unidade': {'type': 'string'},
                                'regiao': {'type': 'string'}
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
def get_producao():
    """Endpoint para obter dados de produção"""
    try:
        service = EmbrapaService()
        page, per_page = get_pagination_params()
        filters = get_filter_params()
        
        data = service.get_data('producao')
        
        if filters.get('ano'):
            data = [item for item in data if item.get('ano') == filters['ano']]
        
        if filters.get('produto'):
            data = [item for item in data if filters['produto'].lower() in item.get('produto', '').lower()]
        
        result = paginate_data(data, page, per_page)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor', 'message': str(e)}), 500

@producao_bp.route('/producao/anos', methods=['GET'])
@optional_token
@swag_from({
    'tags': ['Produção'],
    'summary': 'Obter anos disponíveis',
    'description': 'Retorna lista de anos disponíveis nos dados de produção',
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
def get_producao_anos():
    """Endpoint para obter anos disponíveis nos dados de produção"""
    try:
        service = EmbrapaService()
        data = service.get_data('producao')
        
        anos = sorted(list(set(item.get('ano') for item in data if item.get('ano'))))
        
        return jsonify({'anos': anos}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor', 'message': str(e)}), 500

@producao_bp.route('/producao/produtos', methods=['GET'])
@optional_token
@swag_from({
    'tags': ['Produção'],
    'summary': 'Obter produtos disponíveis',
    'description': 'Retorna lista de produtos disponíveis nos dados de produção',
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
            'description': 'Produtos disponíveis',
            'schema': {
                'type': 'object',
                'properties': {
                    'produtos': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_producao_produtos():
    """Endpoint para obter produtos disponíveis nos dados de produção"""
    try:
        service = EmbrapaService()
        data = service.get_data('producao')
        
        produtos = sorted(list(set(item.get('produto') for item in data if item.get('produto'))))
        
        return jsonify({'produtos': produtos}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor', 'message': str(e)}), 500 