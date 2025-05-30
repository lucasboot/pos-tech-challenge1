from flask import Blueprint, jsonify
from app.services.embrapa_service import EmbrapaService
from app.utils.pagination import get_pagination_params, paginate_data, get_filter_params
from app.utils.auth import optional_token
from flasgger import swag_from

comercializacao_bp = Blueprint('comercializacao', __name__)

@comercializacao_bp.route('/comercializacao', methods=['GET'])
@optional_token
@swag_from({
    'tags': ['Comercialização'],
    'summary': 'Obter dados de comercialização',
    'description': 'Retorna dados de comercialização de vinhos da Embrapa',
    'parameters': [
        {'name': 'page', 'in': 'query', 'type': 'integer', 'description': 'Número da página'},
        {'name': 'per_page', 'in': 'query', 'type': 'integer', 'description': 'Itens por página'},
        {'name': 'ano', 'in': 'query', 'type': 'integer', 'description': 'Filtrar por ano'},
        {'name': 'produto', 'in': 'query', 'type': 'string', 'description': 'Filtrar por produto'}
    ],
    'responses': {200: {'description': 'Dados de comercialização'}}
})
def get_comercializacao():
    try:
        service = EmbrapaService()
        page, per_page = get_pagination_params()
        filters = get_filter_params()
        
        data = service.get_data('comercializacao')
        
        if filters.get('ano'):
            data = [item for item in data if item.get('ano') == filters['ano']]
        
        if filters.get('produto'):
            data = [item for item in data if filters['produto'].lower() in item.get('produto', '').lower()]
        
        result = paginate_data(data, page, per_page)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 