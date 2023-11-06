import os
import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Logger.
from app.logger import configure_log
logger = configure_log()

config_file_path = '/Users/vn54e72/Documents/PERSONAL/proyectos/holywood_grossing_movies_fast_api/app/cfg.cfg'

class DatabaseConnection:

    def __init__(self):
        self._engine = None
        self._session = None
        self._dialect = None
        self._user = None
        self._passwd = None
        self._ip = None
        self._port = None
        self._db = None
        self._db_url = None

    def get_db_connection_config(self):
        if not os.path.exists(config_file_path):
            str_err = f'No existe archivo de configuracion: {config_file_path}.'
            logger.error(str_err)
            raise Exception(str_err)
        
        config = configparser.ConfigParser()
        config.read(config_file_path)

        if config.has_option('DATABASE', 'dialect'):
            self._dialect = config.get('DATABASE', 'dialect')
        else:
            str_err = "Debe indicar el dialecto de la base de datos en DATABASE -> dialect."
            logger.error(str_err)
            raise Exception(str_err)
        
        if config.has_option('DATABASE', 'user'):
            self._user = config.get('DATABASE', 'user')
        else:
            str_err = "Debe indicar el user de la base de datos en DATABASE -> user."
            logger.error(str_err)
            raise Exception(str_err)
        
        if config.has_option('DATABASE', 'pass'):
            self._passwd = config.get('DATABASE', 'pass')
        else:
            str_err = "Debe indicar el passwd de la base de datos en DATABASE -> passwd."
            logger.error(str_err)
            raise Exception(str_err)
        
        if config.has_option('DATABASE', 'ip'):
            self._ip = config.get('DATABASE', 'ip')
        else:
            str_err = "Debe indicar el ip de la base de datos en DATABASE -> ip."
            logger.error(str_err)
            raise Exception(str_err)
        
        if config.has_option('DATABASE', 'port'):
            self._port = config.get('DATABASE', 'port')
        else:
            str_err = "Debe indicar el port de la base de datos en DATABASE -> port."
            logger.error(str_err)
            raise Exception(str_err)
        
        if config.has_option('DATABASE', 'db'):
            self._db = config.get('DATABASE', 'db')
        else:
            str_err = "Debe indicar el db de la base de datos en DATABASE -> db."
            logger.error(str_err)
            raise Exception(str_err)
        
    def get_db_url(self):
        self._db_url = f'{self._dialect}://{self._user}:{self._passwd}@{self._ip}:{self._port}/{self._db}'
      
    def get_engine(self):
        self.get_db_connection_config()
        self.get_db_url()

        if self._engine is None:
            self._engine = create_engine(self._db_url)
    
    def get_session(self):
        self.get_engine()
        Session = sessionmaker(bind=self._engine)
        self._session = Session()
        return self._session

    def close_session(self):
        if not self._engine:
            str_err = 'Ningun engine existente.'
            logger.error(str_err)
            raise Exception(str_err)
        
        if not self._session:
            str_err = 'Ninguna sesion existente.'
            logger.error(str_err)
            raise Exception(str_err)

        self._session.close()
        self._engine.dispose()

        self._engine = None
        self._session = None
        self._dialect = None
        self._user = None
        self._passwd = None
        self._ip = None
        self._port = None
        self._db = None
        self._db_url = None