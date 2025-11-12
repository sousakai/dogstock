import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Caminhos das pastas dentro de 'consulta'
LOGS_DIR = "logs/consulta"         # Logs de leitura (GET)
REGISTRO_DIR = "logs/registro" # Logs de escrita (POST/PUT/DELETE)

# Garante que as pastas existam
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(REGISTRO_DIR, exist_ok=True)

def get_router_logger(router_name: str, registro: bool = False):
    """
    Cria um logger específico para cada router, garantindo que não compartilhe handlers
    com outros loggers existentes, evitando logs na pasta errada.
    """
    # Garante nome único por tipo de logger
    logger_full_name = f"{router_name}_registro" if registro else f"{router_name}_consulta"
    
    logger = logging.getLogger(logger_full_name)
    logger.setLevel(logging.INFO)

    # Se já existir handlers, não adiciona de novo
    if not logger.hasHandlers():
        folder = REGISTRO_DIR if registro else LOGS_DIR
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, f"{router_name}.log")

        handler = TimedRotatingFileHandler(
            filename=file_path,
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - IP: %(ip)s - Método: %(method)s - Status: %(status)s - Mensagem: %(detail)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger