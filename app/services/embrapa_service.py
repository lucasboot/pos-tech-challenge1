import requests
from bs4 import BeautifulSoup
import json
import os
import csv
import io
from datetime import datetime
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class EmbrapaService:
    def __init__(self):
        self.base_url = current_app.config['EMBRAPA_BASE_URL']
        self.cache_dir = 'data/cache'
        self.ensure_cache_dir()
        
        # Mapeamento dos endpoints para URLs e arquivos CSV
        self.endpoint_mapping = {
            'producao': {
                'url': 'index.php?opcao=opt_02',
                'csv_file': 'download/Producao.csv'
            },
            'processamento': {
                'url': 'index.php?opcao=opt_03',
                'csv_file': 'download/ProcessaViniferas.csv'
            },
            'comercializacao': {
                'url': 'index.php?opcao=opt_04',
                'csv_file': 'download/Comercio.csv'
            },
            'importacao': {
                'url': 'index.php?opcao=opt_05',
                'csv_file': 'download/ImpVinhos.csv'
            },
            'exportacao': {
                'url': 'index.php?opcao=opt_06',
                'csv_file': 'download/ExpVinho.csv'
            }
        }
    
    def ensure_cache_dir(self):
        """Garante que o diretório de cache existe"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def get_cached_data(self, endpoint):
        """Recupera dados do cache"""
        cache_file = os.path.join(self.cache_dir, f"{endpoint}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Erro ao ler cache {cache_file}: {e}")
        return None
    
    def save_to_cache(self, endpoint, data):
        """Salva dados no cache"""
        cache_file = os.path.join(self.cache_dir, f"{endpoint}.json")
        try:
            cache_data = {
                'data': data,
                'timestamp': datetime.now().isoformat(),
                'source': 'embrapa_scraping'
            }
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Erro ao salvar cache {cache_file}: {e}")
    
    def download_csv_data(self, endpoint):
        """Baixa e processa dados CSV da Embrapa"""
        try:
            if endpoint not in self.endpoint_mapping:
                logger.error(f"Endpoint {endpoint} não encontrado no mapeamento")
                return None
                
            csv_url = f"{self.base_url}/{self.endpoint_mapping[endpoint]['csv_file']}"
            logger.info(f"Baixando dados de: {csv_url}")
            
            response = requests.get(csv_url, timeout=30)
            response.raise_for_status()
            
            if response.headers.get('content-type', '').startswith('text/html'):
                logger.warning(f"Arquivo CSV não encontrado para {endpoint}")
                return None
            
            csv_content = response.content.decode('utf-8')
            data = self.parse_csv_data(csv_content, endpoint)
            
            return data
            
        except Exception as e:
            logger.error(f"Erro ao baixar dados CSV de {endpoint}: {e}")
            return None
    
    def parse_csv_data(self, csv_content, endpoint):
        """Parse dos dados CSV baseado no endpoint"""
        try:
            if endpoint in ['importacao', 'exportacao']:
                csv_reader = csv.DictReader(io.StringIO(csv_content), delimiter='\t')
            else:
                csv_reader = csv.DictReader(io.StringIO(csv_content), delimiter=';')
            
            data = []
            
            for row in csv_reader:
                if endpoint == 'producao':
                    data.extend(self.parse_producao_row(row))
                elif endpoint == 'processamento':
                    data.extend(self.parse_processamento_row(row))
                elif endpoint == 'comercializacao':
                    data.extend(self.parse_comercializacao_row(row))
                elif endpoint == 'importacao':
                    data.extend(self.parse_importacao_row(row))
                elif endpoint == 'exportacao':
                    data.extend(self.parse_exportacao_row(row))
            
            return data
            
        except Exception as e:
            logger.error(f"Erro ao fazer parse do CSV para {endpoint}: {e}")
            return []
    
    def parse_producao_row(self, row):
        """Parse específico para dados de produção"""
        data = []
        produto = row.get('produto', '').strip()
        
        if not produto or produto.upper() in ['PRODUTO', 'CONTROL']:
            return data
        
        for year in range(1970, 2024):
            year_str = str(year)
            if year_str in row:
                try:
                    quantidade_str = row[year_str].strip()
                    if quantidade_str and quantidade_str not in ['', '0', 'nd', '*']:
                        # Remover caracteres não numéricos exceto vírgula e ponto
                        quantidade_str = quantidade_str.replace(',', '.')
                        quantidade = float(quantidade_str)
                        
                        data.append({
                            'ano': year,
                            'produto': produto,
                            'quantidade': int(quantidade),
                            'unidade': 'litros'
                        })
                except (ValueError, TypeError):
                    continue
        
        return data
    
    def parse_processamento_row(self, row):
        """Parse específico para dados de processamento"""
        data = []
        cultivar = row.get('cultivar', '').strip()
        
        if not cultivar or cultivar.upper() in ['CULTIVAR', 'CONTROL']:
            return data
        
        for year in range(1970, 2024):
            year_str = str(year)
            if year_str in row:
                try:
                    quantidade_str = row[year_str].strip()
                    if quantidade_str and quantidade_str not in ['', '0', 'nd', '*']:
                        quantidade_str = quantidade_str.replace(',', '.')
                        quantidade = float(quantidade_str)
                        
                        data.append({
                            'ano': year,
                            'cultivar': cultivar,
                            'quantidade': int(quantidade),
                            'unidade': 'kg'
                        })
                except (ValueError, TypeError):
                    continue
        
        return data
    
    def parse_comercializacao_row(self, row):
        """Parse específico para dados de comercialização"""
        data = []
        produto = row.get('Produto', '').strip()
        
        if not produto or produto.upper() in ['PRODUTO', 'CONTROL']:
            return data
        
        for year in range(1970, 2024):
            year_str = str(year)
            if year_str in row:
                try:
                    quantidade_str = row[year_str].strip()
                    if quantidade_str and quantidade_str not in ['', '0', 'nd', '*']:
                        quantidade_str = quantidade_str.replace(',', '.')
                        quantidade = float(quantidade_str)
                        
                        data.append({
                            'ano': year,
                            'produto': produto,
                            'quantidade': int(quantidade),
                            'unidade': 'litros'
                        })
                except (ValueError, TypeError):
                    continue
        
        return data
    
    def parse_importacao_row(self, row):
        """Parse específico para dados de importação"""
        data = []
        pais = row.get('País', '').strip()
        
        if not pais or pais.upper() in ['PAÍS', 'CONTROL']:
            return data
        
        # Os arquivos de importação/exportação têm estrutura diferente
        # Cada ano aparece duas vezes (quantidade e valor)
        for year in range(1970, 2025):
            year_str = str(year)
            if year_str in row:
                try:
                    # Primeira coluna do ano é quantidade (kg)
                    quantidade_str = row[year_str].strip()
                    if quantidade_str and quantidade_str not in ['', '0', 'nd', '*']:
                        quantidade_str = quantidade_str.replace(',', '.')
                        quantidade = float(quantidade_str)
                        
                        data.append({
                            'ano': year,
                            'pais': pais,
                            'quantidade': int(quantidade),
                            'unidade': 'kg',
                            'tipo': 'importacao'
                        })
                except (ValueError, TypeError):
                    continue
        
        return data
    
    def parse_exportacao_row(self, row):
        """Parse específico para dados de exportação"""
        data = []
        pais = row.get('País', '').strip()
        
        if not pais or pais.upper() in ['PAÍS', 'CONTROL']:
            return data

        for year in range(1970, 2025):
            year_str = str(year)
            if year_str in row:
                try:
                    quantidade_str = row[year_str].strip()
                    if quantidade_str and quantidade_str not in ['', '0', 'nd', '*']:
                        quantidade_str = quantidade_str.replace(',', '.')
                        quantidade = float(quantidade_str)
                        
                        data.append({
                            'ano': year,
                            'pais': pais,
                            'quantidade': int(quantidade),
                            'unidade': 'kg',
                            'tipo': 'exportacao'
                        })
                except (ValueError, TypeError):
                    continue
        
        return data
    
    def scrape_data(self, endpoint, params=None):
        """Faz scraping dos dados da Embrapa"""
        try:
            data = self.download_csv_data(endpoint)
            
            if data:
                self.save_to_cache(endpoint, data)
                return data
            else:
                logger.warning(f"Não foi possível obter dados CSV para {endpoint}")
                return None
            
        except Exception as e:
            logger.error(f"Erro ao fazer scraping de {endpoint}: {e}")
            return None
    
    def get_data(self, endpoint, params=None, use_cache=True):
        """Método principal para obter dados com fallback"""
        # Tentar scraping primeiro
        data = self.scrape_data(endpoint, params)
        
        if data is None and use_cache:
            # Fallback para cache
            logger.info(f"Usando dados em cache para {endpoint}")
            cached = self.get_cached_data(endpoint)
            if cached:
                return cached['data']
        
        if data is None:
            logger.info(f"Usando dados mock para {endpoint}")
            mock_data = {
                'producao': self.get_mock_producao_data(),
                'processamento': self.get_mock_processamento_data(),
                'comercializacao': self.get_mock_comercializacao_data(),
                'importacao': self.get_mock_importacao_data(),
                'exportacao': self.get_mock_exportacao_data()
            }
            data = mock_data.get(endpoint, [])
        
        return data or []
    
    def get_mock_producao_data(self):
        """Dados mock para produção"""
        return [
            {
                "ano": 2023,
                "produto": "Vinho de mesa",
                "quantidade": 250000000,
                "unidade": "litros",
                "regiao": "Rio Grande do Sul"
            },
            {
                "ano": 2023,
                "produto": "Vinho fino",
                "quantidade": 45000000,
                "unidade": "litros",
                "regiao": "Rio Grande do Sul"
            },
            {
                "ano": 2022,
                "produto": "Vinho de mesa",
                "quantidade": 240000000,
                "unidade": "litros",
                "regiao": "Rio Grande do Sul"
            }
        ]
    
    def get_mock_processamento_data(self):
        """Dados mock para processamento"""
        return [
            {
                "ano": 2023,
                "tipo": "Viníferas",
                "quantidade": 180000000,
                "unidade": "kg",
                "finalidade": "Elaboração"
            },
            {
                "ano": 2023,
                "tipo": "Americanas e híbridas",
                "quantidade": 320000000,
                "unidade": "kg",
                "finalidade": "Elaboração"
            }
        ]
    
    def get_mock_comercializacao_data(self):
        """Dados mock para comercialização"""
        return [
            {
                "ano": 2023,
                "produto": "Vinho de mesa",
                "quantidade": 200000000,
                "unidade": "litros",
                "mercado": "Nacional"
            },
            {
                "ano": 2023,
                "produto": "Espumante",
                "quantidade": 15000000,
                "unidade": "litros",
                "mercado": "Nacional"
            }
        ]
    
    def get_mock_importacao_data(self):
        """Dados mock para importação"""
        return [
            {
                "ano": 2023,
                "produto": "Vinhos de mesa",
                "quantidade": 5000000,
                "unidade": "litros",
                "valor": 15000000,
                "pais_origem": "Argentina"
            },
            {
                "ano": 2023,
                "produto": "Vinhos finos",
                "quantidade": 2000000,
                "unidade": "litros",
                "valor": 25000000,
                "pais_origem": "Chile"
            }
        ]
    
    def get_mock_exportacao_data(self):
        """Dados mock para exportação"""
        return [
            {
                "ano": 2023,
                "produto": "Vinhos de mesa",
                "quantidade": 3000000,
                "unidade": "litros",
                "valor": 12000000,
                "pais_destino": "Paraguai"
            },
            {
                "ano": 2023,
                "produto": "Suco de uva",
                "quantidade": 8000000,
                "unidade": "litros",
                "valor": 20000000,
                "pais_destino": "Estados Unidos"
            }
        ] 