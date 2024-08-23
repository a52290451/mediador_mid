import os
from dotenv import load_dotenv

class Config:
    load_dotenv()  # Carga las variables de entorno desde el archivo .env

    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    TESTING = os.getenv('TESTING', 'False') == 'True'
    API_PORT = os.getenv('API_PORT')

config = Config()