#!/usr/bin/env python3
"""
Script para testar todos os endpoints da API Embrapa
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000/api/v1"

def test_endpoint(endpoint, method="GET", data=None, headers=None):
    """Testa um endpoint específico"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        
        print(f"\n{'='*60}")
        print(f"Endpoint: {method} {endpoint}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Response:")
            # Limitar output para não sobrecarregar
            if isinstance(response_data, dict) and 'data' in response_data:
                data_sample = response_data['data'][:3] if len(response_data['data']) > 3 else response_data['data']
                print(json.dumps({
                    'data': data_sample,
                    'pagination': response_data.get('pagination', {}),
                    'total_records': len(response_data['data']) if 'data' in response_data else 0
                }, indent=2, ensure_ascii=False))
            else:
                print(json.dumps(response_data, indent=2, ensure_ascii=False))
        else:
            print(f"Erro: {response.text}")
        
        return response.json() if response.status_code == 200 else None
        
    except Exception as e:
        print(f"Erro ao testar {endpoint}: {e}")
        return None

def main():
    """Testa todos os endpoints da API"""
    print("🧪 Testando API Vitivinicultura Embrapa")
    print("="*60)
    
    # Teste de autenticação
    print("\n🔐 Testando Autenticação...")
    auth_data = test_endpoint("/auth/login", "POST", {
        "username": "admin",
        "password": "password123"
    }, {"Content-Type": "application/json"})
    
    token = None
    if auth_data and "token" in auth_data:
        token = auth_data["token"]
        print(f"✅ Token obtido: {token[:50]}...")
    
    # Headers com token
    auth_headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    # Teste dos endpoints principais de dados
    print("\n📊 Testando Endpoints Principais...")
    main_endpoints = [
        "/producao",
        "/processamento", 
        "/comercializacao",
        "/importacao",
        "/exportacao"
    ]
    
    for endpoint in main_endpoints:
        test_endpoint(f"{endpoint}?per_page=3", headers=auth_headers)
    
    # Teste dos endpoints de metadados
    print("\n📋 Testando Endpoints de Metadados...")
    metadata_endpoints = [
        "/producao/anos",
        "/producao/produtos",
        "/processamento/anos", 
        "/processamento/cultivares",
        "/comercializacao/anos",
        "/comercializacao/produtos",
        "/importacao/anos",
        "/importacao/paises",
        "/exportacao/anos",
        "/exportacao/paises"
    ]
    
    for endpoint in metadata_endpoints:
        test_endpoint(endpoint, headers=auth_headers)
    
    # Teste com filtros específicos
    print("\n🔍 Testando Filtros Específicos...")
    filter_tests = [
        "/producao?ano=2023&per_page=3",
        "/processamento?cultivar=TINTAS&per_page=3",
        "/comercializacao?produto=VINHO&per_page=3",
        "/importacao?pais=Argentina&per_page=3",
        "/exportacao?ano=2023&per_page=3"
    ]
    
    for endpoint in filter_tests:
        test_endpoint(endpoint, headers=auth_headers)
    
    # Teste de paginação
    print("\n📄 Testando Paginação...")
    test_endpoint("/producao?page=2&per_page=5", headers=auth_headers)
    
    # Teste de validação de token
    if token:
        print("\n✅ Testando Validação de Token...")
        test_endpoint("/auth/validate", headers=auth_headers)
    
    print("\n🎉 Testes concluídos!")
    print(f"📚 Documentação disponível em: http://localhost:5000/apidocs/")
    print(f"🌐 API rodando em: {BASE_URL}")

if __name__ == "__main__":
    main() 