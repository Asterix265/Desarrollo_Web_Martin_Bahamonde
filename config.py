import os
from dotenv import load_dotenv


# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'cc5002'),
    'password': os.getenv('DB_PASSWORD', 'programacionweb'),
    'database': os.getenv('DB_NAME', 'tarea2'),
    'charset': 'utf8mb4'
}

#URL de conexión para SQLAlchemy
DATABASE_URI = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset={DB_CONFIG['charset']}"

# Configuración de archivos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_PHOTOS = 5
MIN_PHOTOS = 1

VALIDATION_RULES = {
    'nombre': {
        'min_length': 3,
        'max_length': 200
    },
    'email': {
        'max_length': 100
    },
    'celular': {
        'max_length': 15
    },
    'sector': {
        'max_length': 100
    },
    'descripcion': {
        'max_length': 500
    },
    'identificador_contacto': {
        'min_length': 4,
        'max_length': 150
    },
    'cantidad_edad': {
        'min_value': 1
    }
}

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
