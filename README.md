# API Vitivinicultura Embrapa

Uma API REST em Python/Flask para consulta de dados de vitivinicultura da Embrapa, desenvolvida como parte do Tech Challenge da Pós-Tech em Machine Learning Engineering.

## 🎯 O Problema em Foco

Esta API foi desenvolvida para facilitar o acesso aos dados de vitivinicultura da Embrapa, fornecendo endpoints estruturados para consulta de informações sobre os tópicos abaixo. Um ponto crucial é reduzir as barreiras no acesso a essas informações, que podem ser de muita valia para produtores menores e até a população geral. 

- **Produção** de vinhos e derivados (1970-2023)
- **Processamento** de uvas por cultivar
- **Comercialização** no mercado nacional
- **Importação** de produtos vitivinícolas por país
- **Exportação** de produtos brasileiros por país

A API serve como fonte de dados para alimentar modelos de Machine Learning e análises de mercado do setor vitivinícola brasileiro. Sendo esse primeiro o próximo objetivo no que diz respeito à evolução desta aplicação.

## ✨ Funcionalidades Implementadas

- ✅ **Scraping Real**: Dados obtidos diretamente dos arquivos CSV da Embrapa
- ✅ **Cache Inteligente**: Sistema de fallback com cache local
- ✅ **Filtros Avançados**: Por ano, produto, cultivar, país
- ✅ **Paginação**: Suporte completo com metadados
- ✅ **Documentação Swagger**: Interface interativa para testes
- ✅ **Autenticação JWT**: Opcional para controle de acesso
- ✅ **Dados Históricos**: Série temporal de 1970 a 2023

## 🛠️ Stack Tecnológica

- **Python 3.11+**
- **Flask** - Framework web
- **Flask-CORS** - Suporte a CORS
- **Flasgger** - Documentação Swagger automática
- **PyJWT** - Autenticação JWT
- **BeautifulSoup4** - Web scraping
- **Requests** - Cliente HTTP
- **Gunicorn** - Servidor WSGI para produção
- **Docker** - Containerização

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.11+
- pip
- Docker (opcional)

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/pos-tech-challenge1.git
cd pos-tech-challenge1
```

### 2. Criar Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

### 5. Executar a Aplicação
```bash
python run.py
```

A API estará disponível em `http://localhost:5000`

## 🐳 Executar com Docker

### Usando Docker Compose (Recomendado)

```bash
# Primeira execução - construir e executar
docker-compose up --build

# Parar os serviços
docker-compose down

# Executar novamente (sem rebuild)
docker-compose up

# Executar em background
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### Usando Docker Tradicional (Alternativo)

```bash
# 1. Construir a Imagem
docker build -t embrapa-api .

# 2. Executar o Container
docker run -p 5000:5000 embrapa-api
```

## 📚 Documentação da API

A documentação completa da API está disponível via Swagger em:
- **Local**: `http://localhost:5000/apidocs/`
- **Produção**: [Link da API em produção]/apidocs/

### Endpoints Principais

#### Autenticação
- `POST /api/v1/auth/login` - Login e obtenção de token JWT
- `GET /api/v1/auth/validate` - Validação de token

#### Dados de Produção
- `GET /api/v1/producao` - Dados de produção de vinhos e derivados
- `GET /api/v1/producao/anos` - Anos disponíveis nos dados de produção
- `GET /api/v1/producao/produtos` - Produtos disponíveis

#### Dados de Processamento
- `GET /api/v1/processamento` - Dados de processamento de uvas por cultivar
- `GET /api/v1/processamento/anos` - Anos disponíveis nos dados de processamento
- `GET /api/v1/processamento/cultivares` - Cultivares disponíveis

#### Dados de Comercialização
- `GET /api/v1/comercializacao` - Dados de comercialização no mercado nacional
- `GET /api/v1/comercializacao/anos` - Anos disponíveis nos dados de comercialização
- `GET /api/v1/comercializacao/produtos` - Produtos disponíveis

#### Dados de Importação
- `GET /api/v1/importacao` - Dados de importação por país
- `GET /api/v1/importacao/anos` - Anos disponíveis nos dados de importação
- `GET /api/v1/importacao/paises` - Países de origem disponíveis

#### Dados de Exportação
- `GET /api/v1/exportacao` - Dados de exportação por país
- `GET /api/v1/exportacao/anos` - Anos disponíveis nos dados de exportação
- `GET /api/v1/exportacao/paises` - Países de destino disponíveis

### Parâmetros de Consulta

#### Parâmetros Comuns (todos os endpoints)
- `page` - Número da página (padrão: 1)
- `per_page` - Itens por página (padrão: 50, máximo: 1000)
- `ano` - Filtrar por ano específico

#### Parâmetros Específicos
- **Produção/Comercialização**: `produto` - Filtrar por produto
- **Processamento**: `cultivar` - Filtrar por cultivar
- **Importação/Exportação**: `pais` - Filtrar por país

### Exemplos de Uso

```bash
# Obter dados de produção de 2023
curl "http://localhost:5000/api/v1/producao?ano=2023&per_page=10"

# Filtrar processamento por cultivar
curl "http://localhost:5000/api/v1/processamento?cultivar=Cabernet"

# Importações da Argentina
curl "http://localhost:5000/api/v1/importacao?pais=Argentina"

# Listar todos os países de exportação
curl "http://localhost:5000/api/v1/exportacao/paises"
```

### Estrutura de Resposta

```json
{
  "data": [
    {
      "ano": 2023,
      "produto": "VINHO DE MESA",
      "quantidade": 169762429,
      "unidade": "litros"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 1100,
    "pages": 22,
    "has_prev": false,
    "has_next": true
  }
}
```

### Autenticação

A API suporta autenticação JWT opcional. Para obter um token:

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password123"}'
```

Use o token nas requisições:
```bash
curl -H "Authorization: Bearer SEU_TOKEN" \
  http://localhost:5000/api/v1/producao
```

## Estrutura de pastas do Projeto

```
pos-tech-challenge1/
├── app/
│   ├── __init__.py          # Factory da aplicação Flask
│   ├── config.py            # Configurações
│   ├── routes/              # Blueprints das rotas
│   │   ├── auth_routes.py
│   │   ├── producao_routes.py
│   │   ├── processamento_routes.py
│   │   ├── comercializacao_routes.py
│   │   ├── importacao_routes.py
│   │   └── exportacao_routes.py
│   ├── services/            # Lógica de negócio
│   │   └── embrapa_service.py
│   └── utils/               # Utilitários
│       ├── auth.py          # Autenticação JWT
│       └── pagination.py    # Paginação
├── data/cache/              # Cache local (fallback)
├── requirements.txt         # Dependências Python
├── Dockerfile              # Container Docker
├── vercel.json             # Configuração Vercel
├── run.py                  # Ponto de entrada
└── README.md               # Este arquivo
```

## 🏗️ Arquitetura do Projeto

![mermaid-diagram-2025-05-31-195956](https://github.com/user-attachments/assets/3202a63e-af05-4daa-bd1d-2d84f406103b)

## 🔄 Sistema de Dados e Cache

A API implementa um sistema robusto de obtenção de dados:

1. **Scraping Real**: Baixa dados diretamente dos arquivos CSV da Embrapa
   - `Producao.csv` - Dados de produção (separador: `;`)
   - `ProcessaViniferas.csv` - Processamento de cultivares (separador: `;`)
   - `Comercio.csv` - Comercialização (separador: `;`)
   - `ImpVinhos.csv` - Importação (separador: `\t`)
   - `ExpVinho.csv` - Exportação (separador: `\t`)

2. **Cache Local**: Se o scraping falhar, usa dados em cache local
3. **Fallback Mock**: Para desenvolvimento, fornece dados de exemplo

## 📊 Volume de Dados Disponíveis

- **Produção**: 1.100+ registros (1970-2023)
- **Processamento**: 3.022+ registros de cultivares
- **Comercialização**: 1.836+ registros
- **Importação**: 964+ registros por país
- **Exportação**: 1.421+ registros por país

## 🚀 Deploy

### Vercel (Recomendado)

1. Instale a CLI da Vercel: `npm i -g vercel`
2. Execute: `vercel --prod`
3. Configure as variáveis de ambiente no dashboard da Vercel

### Outras Plataformas

A aplicação é compatível com:
- **Heroku**
- **Railway**
- **Render**
- **Google Cloud Run**
- **AWS Lambda** (com adaptações)

## 🧪 Testes

Para executar os testes (ainda não foram implementados!!!):
```bash
pytest
```

## 📊 Casos de Uso para Machine Learning

Esta API pode alimentar modelos de ML para:

1. **Previsão de Safras**: Análise de tendências de produção, disponibilidade de produtos
2. **Análise de Mercado**: Padrões de importação/exportação
3. **Otimização de Preços**: Correlação entre o que for produzido e o que foi vendido
4. **Detecção de Anomalias**: Identificação de novos padrões
5. **Forecasting**: Previsão de demanda e oferta
6. **Análise de Cultivares**: Performance de diferentes tipos de uva
7. **Mercado Internacional**: Tendências de importação/exportação por país

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Link da API em Produção**: [Será atualizado após deploy]

**Documentação Swagger**: `http://localhost:5000/apidocs/`
