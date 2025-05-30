from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from app.config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configurar CORS
    CORS(app)
    
    # Detectar se está rodando na Vercel
    is_vercel = os.environ.get('VERCEL') == '1'
    
    # Configurar Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    # Configurar host dinamicamente
    if is_vercel:
        host = os.environ.get('VERCEL_URL', 'localhost:5000')
        if not host.startswith('http'):
            host = f"https://{host}"
        schemes = ["https"]
    else:
        host = "localhost:5000"
        schemes = ["http", "https"]
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API Vitivinicultura Embrapa",
            "description": "API para consulta de dados de vitivinicultura da Embrapa",
            "version": "1.0.0"
        },
        "host": host.replace('https://', '').replace('http://', ''),
        "basePath": "/",
        "schemes": schemes
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Registrar blueprint home primeiro (para rota raiz)
    from app.routes.home_routes import home_bp
    app.register_blueprint(home_bp)
    
    # Registrar outros blueprints
    from app.routes.producao_routes import producao_bp
    from app.routes.processamento_routes import processamento_bp
    from app.routes.comercializacao_routes import comercializacao_bp
    from app.routes.importacao_routes import importacao_bp
    from app.routes.exportacao_routes import exportacao_bp
    from app.routes.auth_routes import auth_bp
    
    app.register_blueprint(producao_bp, url_prefix='/api/v1')
    app.register_blueprint(processamento_bp, url_prefix='/api/v1')
    app.register_blueprint(comercializacao_bp, url_prefix='/api/v1')
    app.register_blueprint(importacao_bp, url_prefix='/api/v1')
    app.register_blueprint(exportacao_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1')
    
    return app 