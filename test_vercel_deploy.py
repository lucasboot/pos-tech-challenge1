#!/usr/bin/env python3
"""
Teste específico para verificar se o deploy na Vercel está funcionando
Execute: python test_vercel_deploy.py
"""

import requests
import sys
import json

def test_vercel_deployment(base_url):
    """Testa se o deployment na Vercel está funcionando"""
    
    print(f"🧪 Testando deployment em: {base_url}")
    print("=" * 50)
    
    tests = [
        {
            "name": "Rota raiz (/)",
            "url": f"{base_url}/",
            "expected_status": 200,
            "expected_content": "API Vitivinicultura Embrapa"
        },
        {
            "name": "Health check (/health)",
            "url": f"{base_url}/health",
            "expected_status": 200,
            "expected_content": "healthy"
        },
        {
            "name": "Documentação Swagger (/apidocs/)",
            "url": f"{base_url}/apidocs/",
            "expected_status": 200,
            "expected_content": "swagger"
        },
        {
            "name": "API Spec (/apispec.json)",
            "url": f"{base_url}/apispec.json",
            "expected_status": 200,
            "expected_content": "swagger"
        },
        {
            "name": "Endpoint de produção (/api/v1/producao)",
            "url": f"{base_url}/api/v1/producao",
            "expected_status": 200,
            "expected_content": None  # Pode variar dependendo dos dados
        }
    ]
    
    results = []
    
    for test in tests:
        print(f"🔍 Testando: {test['name']}")
        
        try:
            response = requests.get(test['url'], timeout=30)
            
            # Verificar status code
            status_ok = response.status_code == test['expected_status']
            
            # Verificar conteúdo se especificado
            content_ok = True
            if test['expected_content']:
                content_ok = test['expected_content'].lower() in response.text.lower()
            
            if status_ok and content_ok:
                print(f"   ✅ PASSOU - Status: {response.status_code}")
                results.append(True)
            else:
                print(f"   ❌ FALHOU - Status: {response.status_code}")
                if not content_ok:
                    print(f"      Conteúdo esperado '{test['expected_content']}' não encontrado")
                results.append(False)
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ ERRO - {str(e)}")
            results.append(False)
        
        print()
    
    # Resumo
    passed = sum(results)
    total = len(results)
    
    print("=" * 50)
    print(f"📊 RESUMO: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Deploy está funcionando corretamente.")
        return True
    else:
        print("⚠️  Alguns testes falharam. Verifique a configuração.")
        return False

def main():
    if len(sys.argv) != 2:
        print("Uso: python test_vercel_deploy.py <URL_DA_VERCEL>")
        print("Exemplo: python test_vercel_deploy.py https://seu-projeto.vercel.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    success = test_vercel_deployment(base_url)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 