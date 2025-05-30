from flask import Blueprint, redirect, jsonify

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
def home():
    """
    Rota principal da API
    ---
    tags:
      - Home
    responses:
      200:
        description: Informações da API
        schema:
          type: object
          properties:
            message:
              type: string
              example: "API Vitivinicultura Embrapa"
            version:
              type: string
              example: "1.0.0"
            documentation:
              type: string
              example: "/apidocs/"
            endpoints:
              type: object
              properties:
                producao:
                  type: string
                  example: "/api/v1/producao"
                processamento:
                  type: string
                  example: "/api/v1/processamento"
                comercializacao:
                  type: string
                  example: "/api/v1/comercializacao"
                importacao:
                  type: string
                  example: "/api/v1/importacao"
                exportacao:
                  type: string
                  example: "/api/v1/exportacao"
                auth:
                  type: string
                  example: "/api/v1/auth"
    """
    return jsonify({
        "message": "API Vitivinicultura Embrapa",
        "version": "1.0.0",
        "documentation": "/apidocs/",
        "endpoints": {
            "producao": "/api/v1/producao",
            "processamento": "/api/v1/processamento", 
            "comercializacao": "/api/v1/comercializacao",
            "importacao": "/api/v1/importacao",
            "exportacao": "/api/v1/exportacao",
            "auth": "/api/v1/auth"
        }
    })

@home_bp.route('/health', methods=['GET'])
def health():
    """
    Health check da API
    ---
    tags:
      - Health
    responses:
      200:
        description: Status da API
        schema:
          type: object
          properties:
            status:
              type: string
              example: "healthy"
            timestamp:
              type: string
              example: "2024-01-01T00:00:00Z"
    """
    from datetime import datetime
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }) 