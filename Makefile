.PHONY: help install run test docker-build docker-run docker-stop clean

# Variáveis
PYTHON = python3
VENV = venv
PIP = $(VENV)/bin/pip
PYTHON_VENV = $(VENV)/bin/python

help: 
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: 
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: 
	$(PYTHON_VENV) run.py

test: 
	$(PYTHON_VENV) test_api.py

docker-build: 
	docker build -t embrapa-api .

docker-run: 
	docker run -p 5000:5000 --name embrapa-api-container embrapa-api

docker-compose-up: 
	docker-compose up --build

docker-compose-down: 
	docker-compose down

docker-stop:
	docker stop embrapa-api-container || true
	docker rm embrapa-api-container || true

clean: 
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf $(VENV)

dev-setup: install 
	cp env.example .env
	@echo "✅ Ambiente configurado!"
	@echo "📝 Edite o arquivo .env com suas configurações"
	@echo "🚀 Execute 'make run' para iniciar a aplicação"

deploy-vercel: 
	vercel --prod

format: 
	$(PYTHON_VENV) -m black app/ --line-length 88

lint:
	$(PYTHON_VENV) -m flake8 app/ --max-line-length=88 