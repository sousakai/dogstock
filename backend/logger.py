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
    Cria logger específico para cada router.
    
    Parâmetros:
    - router_name: nome do router (nome do arquivo de log)
    - registro: False para logs de leitura, True para logs de escrita
    """
    logger = logging.getLogger(router_name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Escolhe a pasta correta
        folder = REGISTRO_DIR if registro else LOGS_DIR
        os.makedirs(folder, exist_ok=True)  # garante que a pasta exista
        file_path = os.path.join(folder, f"{router_name}.log")

        # Handler com rotação diária
        handler = TimedRotatingFileHandler(
            filename=file_path,
            when="midnight",  # cria novo arquivo à meia-noite
            interval=1,
            backupCount=7,    # mantém 7 arquivos antigos
            encoding="utf-8"
        )

        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - IP: %(ip)s - Método: %(method)s - Status: %(status)s - Mensagem: %(detail)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
