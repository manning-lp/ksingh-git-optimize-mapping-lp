import os
import sys
import logging

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, "modules/"
)
sys.path.append(SOURCE_PATH)

from importer import verify_connection, import_shoes_from_file
from dotenv import load_dotenv
from logging import config
from log_config import logging_config


load_dotenv()

config.dictConfig(logging_config)

run_logging = logging.getLogger("runner")

if __name__ == '__main__':
    run_logging.info('Started the importer')
    verify_connection()
    import_shoes_from_file(file_name='./data/shoes.mjson')
    run_logging.info('Finished the importer')
