# 🔧 Troubleshooting - Deploy Vercel

## ❌ Problema: Erro 404 em todas as rotas

### Sintomas:
- Todas as rotas retornam 404
- Logs mostram `"GET / HTTP/1.1" 404 -`
- Swagger não carrega

### ✅ Solução Aplicada:

1. **Adicionada rota raiz (`/`)** no arquivo `app/routes/home_routes.py`
2. **Configuração dinâmica do Swagger** para detectar ambiente Vercel
3. **Atualizado `vercel.json`** com variável `VERCEL=1`

### 🔍 Como Verificar se Foi Corrigido:

```bash
# Teste local primeiro
./scripts/test-deploy.sh

# Após deploy, teste na Vercel
python test_vercel_deploy.py https://seu-projeto.vercel.app
```

## 🚨 Outros Problemas Comuns

### 1. Swagger não carrega na Vercel

**Problema**: Swagger funciona localmente mas não na Vercel

**Solução**:
- ✅ Configuração dinâmica de host implementada
- ✅ Detecção automática do ambiente Vercel
- ✅ Esquemas HTTPS configurados para produção

### 2. Timeout nas funções

**Problema**: Funções excedem tempo limite

**Solução**:
```json
// vercel.json
"functions": {
  "run.py": {
    "maxDuration": 30
  }
}
```

### 3. Variáveis de ambiente não carregam

**Problema**: Configurações não são aplicadas

**Verificar**:
1. Variáveis configuradas no dashboard da Vercel
2. Arquivo `.env` não é usado na Vercel (apenas local)
3. Usar `os.environ.get()` no código

### 4. Imports não funcionam

**Problema**: Módulos não são encontrados

**Solução**:
- ✅ Estrutura de imports relativa implementada
- ✅ `__init__.py` em todas as pastas
- ✅ Blueprints registrados corretamente

## 📋 Checklist de Deploy

Antes de fazer deploy, verifique:

- [ ] ✅ Rota raiz (`/`) existe e funciona
- [ ] ✅ `requirements.txt` atualizado
- [ ] ✅ Testes passando localmente
- [ ] ✅ Variáveis de ambiente configuradas na Vercel
- [ ] ✅ `vercel.json` configurado corretamente

## 🧪 Comandos de Teste

### Teste Local Completo
```bash
chmod +x scripts/test-deploy.sh
./scripts/test-deploy.sh
```

### Teste do Deploy na Vercel
```bash
python test_vercel_deploy.py https://seu-projeto.vercel.app
```

### Teste Manual das Rotas
```bash
# Rota principal
curl https://seu-projeto.vercel.app/

# Health check
curl https://seu-projeto.vercel.app/health

# Swagger
curl https://seu-projeto.vercel.app/apidocs/

# API endpoints
curl https://seu-projeto.vercel.app/api/v1/producao
```

## 📊 Logs da Vercel

### Como Acessar:
1. Dashboard da Vercel > Seu Projeto
2. Aba "Functions"
3. Clique em qualquer função para ver logs

### O que Procurar:
- ✅ Status 200 para rotas principais
- ❌ Status 404 indica rota não encontrada
- ❌ Status 500 indica erro interno

### Logs Normais Após Correção:
```
"GET /" 200 - Rota principal funcionando
"GET /health" 200 - Health check OK
"GET /apidocs/" 200 - Swagger carregando
"GET /api/v1/producao" 200 - API funcionando
```

## 🔄 Redeployment

Se ainda houver problemas após as correções:

1. **Force redeploy**:
   ```bash
   git commit --allow-empty -m "trigger redeploy"
   git push origin main
   ```

2. **Limpar cache da Vercel**:
   - Dashboard > Settings > Advanced
   - "Clear Build Cache"

3. **Verificar build logs**:
   - Dashboard > Deployments
   - Clique no deployment mais recente
   - Verifique "Build Logs"

## 📞 Suporte

Se o problema persistir:

1. Verifique os logs detalhados na Vercel
2. Execute `python test_vercel_deploy.py` para diagnóstico
3. Compare com funcionamento local usando `./scripts/test-deploy.sh`

---

**🎯 Com as correções aplicadas, o erro 404 deve estar resolvido!** 