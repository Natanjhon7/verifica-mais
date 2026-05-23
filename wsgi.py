import sys
import os

# Adiciona o diretório do projeto ao path
path = '/home/SEU_USUARIO/verifica-mais'
if path not in sys.path:
    sys.path.insert(0, path)

# Carrega variáveis de ambiente
from dotenv import load_dotenv
env_path = os.path.join(path, '.env')
load_dotenv(env_path)

# Importa o app
from app import app as application