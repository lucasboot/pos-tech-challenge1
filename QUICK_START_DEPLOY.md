# 🚀 Guia Rápido - Deploy Automático Vercel + GitHub Actions

## ⚡ Comandos Rápidos

### 1. Tornar o script executável e testar localmente
```bash
chmod +x scripts/test-deploy.sh
./scripts/test-deploy.sh
```

### 2. Fazer commit das configurações (INCLUINDO CORREÇÃO 404)
```bash
git add .
git commit -m "fix: adicionar rota raiz e corrigir configuração Vercel para resolver erro 404"
git push origin main
```

### 3. Testar o deploy na Vercel
```bash
python test_vercel_deploy.py https://seu-projeto.vercel.app
```

## 🔑 Secrets Necessários no GitHub

Vá em: **Repositório > Settings > Secrets and variables > Actions**

Adicione estes 3 secrets:

| Nome | Onde encontrar |
|------|----------------|
| `VERCEL_TOKEN` | [vercel.com/account/tokens](https://vercel.com/account/tokens) |
| `VERCEL_ORG_ID` | [vercel.com/account](https://vercel.com/account) (Team/User ID) |
| `VERCEL_PROJECT_ID` | Projeto na Vercel > Settings > General |

## 🛠️ Correções Aplicadas para Erro 404

✅ **Problema resolvido**: Erro 404 em todas as rotas

**O que foi corrigido:**
- ➕ Adicionada rota raiz (`/`) em `app/routes/home_routes.py`
- ⚙️ Configuração dinâmica do Swagger para Vercel
- 🔧 Atualizado `vercel.json` com detecção de ambiente
- 🧪 Criados testes específicos para Vercel

## 📁 Arquivos Criados/Atualizados

- `.github/workflows/deploy.yml` - Workflow do GitHub Actions
- `app/routes/home_routes.py` - **NOVO**: Rota raiz e health check
- `app/__init__.py` - **ATUALIZADO**: Configuração dinâmica Swagger
- `vercel.json` - **ATUALIZADO**: Configuração melhorada
- `test_vercel_deploy.py` - **NOVO**: Teste específico para Vercel
- `scripts/test-deploy.sh` - **ATUALIZADO**: Testes mais completos
- `VERCEL_TROUBLESHOOTING.md` - **NOVO**: Guia de troubleshooting

## 🎯 Como Funciona Agora

1. **Push para main/master** → Deploy de produção
2. **Pull Request** → Deploy de preview
3. **Testes automáticos** antes de cada deploy
4. **Rota raiz (`/`)** → Retorna informações da API
5. **Health check (`/health`)** → Status da aplicação
6. **Swagger (`/apidocs/`)** → Documentação interativa

## 🔍 Verificar Deploy

### Rotas que devem funcionar:
- **`/`** - Informações da API
- **`/health`** - Health check
- **`/apidocs/`** - Documentação Swagger
- **`/api/v1/producao`** - Endpoint de produção
- **`/api/v1/processamento`** - Endpoint de processamento

### Ferramentas de verificação:
- **GitHub**: Aba "Actions" do repositório
- **Vercel**: Dashboard do projeto
- **Teste automatizado**: `python test_vercel_deploy.py <URL>`

## 🚨 Se ainda houver problemas

1. **Consulte**: `VERCEL_TROUBLESHOOTING.md`
2. **Execute**: `python test_vercel_deploy.py <URL_DA_VERCEL>`
3. **Verifique logs**: Dashboard Vercel > Functions

---

**🎉 Agora o erro 404 está corrigido! Faça push e teste!** 