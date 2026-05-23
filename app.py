# app.py (na raiz do projeto)
import sys
import os

# Adiciona o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Importa o app do backend
from backend.app import app, application