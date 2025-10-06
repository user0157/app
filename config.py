import os
import sys
from dotenv import load_dotenv

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Carregar variáveis do .env
dotenv_path = resource_path(".env")
load_dotenv(dotenv_path)

# Variáveis comuns
APP_NAME = os.getenv("APP_NAME", "未知应用")
VERSION = os.getenv("VERSION", "0.0.0")
AUTHOR = os.getenv("AUTHOR", "未知作者")

# Verifica o ambiente: 'production' ou 'test'
MODE = os.getenv("MODE", "production").lower()

if MODE == "test":
    API_URL = os.getenv("API_TEST")
else:
    API_URL = os.getenv("API_URL")
