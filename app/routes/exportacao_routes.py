from flask import Blueprint, jsonify
from app.services.embrapa_service import EmbrapaService
from app.utils.pagination import get_pagination_params, paginate_data, get_filter_params
from app.utils.auth import optional_token
from flasgger import swag_from

exportacao_bp = Blueprint('exportacao', __name__)

@exportacao_bp.route('/exportacao', methods=['GET'])
@optional_token
@swag_from({
    'tags': ['Exportação'],
    'summary': 'Obter dados de exportação',
    'description': 'Retorna dados de exportação de vinhos da Embrapa com suporte a paginação e filtros',
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
            'name': 'pais',
            'in': 'query',
            'type': 'string',
            'description': 'Filtrar por país de destino'
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
            'description': 'Dados de exportação retornados com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'ano': {'type': 'integer'},
                                'pais': {'type': 'string'},
                                'quantidade': {'type': 'integer'},
                                'unidade': {'type': 'string'},
                                'tipo': {'type': 'string'}
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
def get_exportacao():
    """Endpoint para obter dados de exportação"""
    try:
        service = EmbrapaService()
        page, per_page = get_pagination_params()
        filters = get_filter_params()
        
        data = service.get_data('exportacao')
        
        if filters.get('ano'):
            data = [item for item in data if item.get('ano') == filters['ano']]
        
        if filters.get('pais'):
            data = [item for item in data if filters['pais'].lower() in item.get('pais', '').lower()]
        
        result = paginate_data(data, page, per_page)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor', 'message': str(e)}), 500

@exportacao_bp.route('/exportacao/anos', methods=['GET'])
@optional_token
@swag_from({
    'tags': ['Exportação'],
    'summary': 'Obter anos disponíveis',
    'description': 'Retorna lista de anos disponíveis nos dados de exportação',
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
def get_exportacao_anos():
    """Endpoint para obter anos disponíveis nos dados de exportação"""
    try:
        service = EmbrapaService()
        data = service.get_data('exportacao')
        
        anos = sorted(list(set(item.get('ano') for item in data if item.get('ano'))))
        
        return jsonify({'anos': anos}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor', 'message': str(e)}), 500

@exportacao_bp.route('/exportacao/paises', methods=['GET'])
@optional_token
@swag_from({
    'tags': ['Exportação'],
    'summary': 'Obter países disponíveis',
    'description': 'Retorna lista de países disponíveis nos dados de exportação',
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
            'description': 'Países disponíveis',
            'schema': {
                'type': 'object',
                'properties': {
                    'paises': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_exportacao_paises():
    """Endpoint para obter países disponíveis nos dados de exportação"""
    try:
        service = EmbrapaService()
        data = service.get_data('exportacao')
        
        paises = sorted(list(set(item.get('pais') for item in data if item.get('pais'))))
        
        return jsonify({'paises': paises}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor', 'message': str(e)}), 500 