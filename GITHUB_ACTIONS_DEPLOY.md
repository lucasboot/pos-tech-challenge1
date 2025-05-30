# Deploy Automático na Vercel via GitHub Actions

Este guia explica como configurar o deploy automático da aplicação na Vercel através do GitHub Actions.

## 📋 Pré-requisitos

1. Conta na [Vercel](https://vercel.com)
2. Repositório no GitHub
3. Projeto já configurado localmente

## 🚀 Configuração Passo a Passo

### 1. Configurar o Projeto na Vercel

1. Acesse [vercel.com](https://vercel.com) e faça login
2. Clique em "New Project"
3. Importe seu repositório do GitHub
4. Configure as seguintes variáveis de ambiente na Vercel:
   - `FLASK_ENV=production`
   - Adicione outras variáveis necessárias do seu `env.example`

### 2. Obter os Tokens e IDs Necessários

#### 2.1 Vercel Token
1. Vá para [Vercel Settings > Tokens](https://vercel.com/account/tokens)
2. Clique em "Create Token"
3. Dê um nome (ex: "GitHub Actions")
4. Copie o token gerado

#### 2.2 Organization ID
1. Vá para [Vercel Settings > General](https://vercel.com/account)
2. Copie o "Team ID" (ou "User ID" se for conta pessoal)

#### 2.3 Project ID
1. Acesse seu projeto na Vercel
2. Vá em Settings > General
3. Copie o "Project ID"

### 3. Configurar Secrets no GitHub

1. Vá para seu repositório no GitHub
2. Clique em "Settings" > "Secrets and variables" > "Actions"
3. Clique em "New repository secret" e adicione:

```
VERCEL_TOKEN: [seu token da vercel]
VERCEL_ORG_ID: [seu organization/user ID]
VERCEL_PROJECT_ID: [seu project ID]
```

### 4. Como Funciona o Workflow

O workflow configurado irá:

- **Em Pull Requests**: Criar um deploy de preview
- **Em push para main/master**: Fazer deploy para produção
- **Executar testes**: Antes de cada deploy
- **Instalar dependências**: Automaticamente

### 5. Estrutura do Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - Checkout do código
      - Setup do Python
      - Instalação de dependências
      - Execução de testes
      - Deploy na Vercel
```

## 🔧 Personalização

### Adicionar Variáveis de Ambiente

Se sua aplicação precisar de variáveis de ambiente específicas, adicione-as:

1. Na Vercel (para runtime)
2. Como secrets no GitHub (se necessário para build/testes)

### Modificar Condições de Deploy

Para alterar quando o deploy acontece, modifique as seções `on:` e `if:` no workflow.

### Adicionar Mais Testes

Para adicionar mais verificações antes do deploy:

```yaml
- name: Lint code
  run: |
    pip install flake8
    flake8 app/ --max-line-length=88

- name: Security check
  run: |
    pip install safety
    safety check
```

## 🚨 Troubleshooting

### Erro de Token Inválido
- Verifique se o `VERCEL_TOKEN` está correto
- Certifique-se de que o token não expirou

### Erro de Project ID
- Confirme se o `VERCEL_PROJECT_ID` está correto
- Verifique se o projeto existe na Vercel

### Falha nos Testes
- O deploy não acontecerá se os testes falharem
- Verifique os logs do GitHub Actions para detalhes

### Deploy não Acontece
- Verifique se o push foi para a branch correta (main/master)
- Confirme se todos os secrets estão configurados

## 📝 Comandos Úteis

### Testar Localmente
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar testes
python -m pytest test_api.py -v

# Executar aplicação
python run.py
```

### Verificar Status do Deploy
- Acesse a aba "Actions" no seu repositório GitHub
- Veja os logs detalhados de cada execução

## 🔗 Links Úteis

- [Documentação Vercel CLI](https://vercel.com/docs/cli)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Vercel Python Runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)

---

**Nota**: Após configurar tudo, faça um commit e push para testar o workflow! 