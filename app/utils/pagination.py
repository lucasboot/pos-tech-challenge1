from flask import request, current_app
from math import ceil

def get_pagination_params():
    """Extrai parâmetros de paginação da requisição"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', current_app.config['DEFAULT_PAGE_SIZE'], type=int)
    
    # Limitar o tamanho máximo da página
    if per_page > current_app.config['MAX_PAGE_SIZE']:
        per_page = current_app.config['MAX_PAGE_SIZE']
    
    # Garantir valores mínimos
    page = max(1, page)
    per_page = max(1, per_page)
    
    return page, per_page

def paginate_data(data, page, per_page):
    """Pagina uma lista de dados"""
    total = len(data)
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_data = data[start:end]
    
    return {
        'data': paginated_data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': ceil(total / per_page),
            'has_prev': page > 1,
            'has_next': page < ceil(total / per_page)
        }
    }

def get_filter_params():
    """Extrai parâmetros de filtro da requisição"""
    filters = {}
    
    # Filtros comuns
    ano = request.args.get('ano', type=int)
    if ano:
        filters['ano'] = ano
    
    categoria = request.args.get('categoria')
    if categoria:
        filters['categoria'] = categoria
    
    produto = request.args.get('produto')
    if produto:
        filters['produto'] = produto
    
    cultivar = request.args.get('cultivar')
    if cultivar:
        filters['cultivar'] = cultivar
    
    pais = request.args.get('pais')
    if pais:
        filters['pais'] = pais
    
    return filters 