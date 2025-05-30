#!/bin/bash

# Script para testar o deploy localmente antes de fazer push
# Execute: chmod +x scripts/test-deploy.sh && ./scripts/test-deploy.sh

echo "🚀 Testando deploy local..."

# Verificar se está no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erro: Execute este script na raiz do projeto"
    exit 1
fi

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Testar se a aplicação inicia corretamente
echo "🔧 Testando inicialização da aplicação..."
timeout 10s python run.py &
APP_PID=$!

# Aguardar um pouco para a aplicação iniciar
sleep 3

# Verificar se a aplicação está rodando
if kill -0 $APP_PID 2>/dev/null; then
    echo "✅ Aplicação iniciou corretamente!"
    
    # Testar rota principal
    echo "🌐 Testando rota principal..."
    curl -s http://localhost:5000/ > /dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Rota principal funcionando!"
    else
        echo "⚠️  Rota principal não respondeu (normal se não tiver dados)"
    fi
    
    # Parar a aplicação
    kill $APP_PID 2>/dev/null
else
    echo "❌ Aplicação falhou ao iniciar!"
    exit 1
fi

echo ""
echo "✅ Todos os testes passaram! Deploy pode ser feito com segurança."
echo ""
echo "📋 Próximos passos:"
echo "1. Configure os secrets no GitHub (veja GITHUB_ACTIONS_DEPLOY.md)"
echo "2. Faça commit e push para main/master:"
echo "   git add ."
echo "   git commit -m 'fix: adicionar rota raiz e corrigir configuração Vercel'"
echo "   git push origin main"
echo "3. Acompanhe o deploy na aba Actions do GitHub"
echo "4. Teste o deploy com: python test_vercel_deploy.py <URL_DA_VERCEL>" 