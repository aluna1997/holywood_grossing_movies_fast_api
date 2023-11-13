import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.logger import configure_log
from app.common.utils_common import get_value_from_config_file

# Logger..
logger = configure_log()

class DatabaseConnection:
    '''
    Represents a utility class for managing database connections and sessions.

    This class provides methods to configure and establish a database connection, create a SQLAlchemy
    engine, and manage database sessions. It is intended for use with SQLAlchemy to simplify database
    operations.

    Attributes:
        _engine: The SQLAlchemy engine used for connecting to the database.
        _session: The active SQLAlchemy session.
        _dialect: The database dialect (e.g., MySQL, PostgreSQL).
        _user: The database username for authentication.
        _passwd: The database password for authentication.
        _ip: The IP address or hostname of the database server.
        _port: The port number on which the database server is running.
        _db: The name of the database to connect to.
        _db_url: The complete database connection URL constructed from the above attributes.

    Methods:
        get_db_connection_config(): Reads database connection configuration from a config file and sets
        class attributes such as dialect, user, password, IP, port, and database name.

        get_db_url(): Constructs the database connection URL using the configured attributes.

        get_engine(): Creates an SQLAlchemy engine based on the constructed database connection URL.

        get_session(): Creates an SQLAlchemy session for database interactions using the established engine.

        close_session(): Closes the active session and disposes of the engine, resetting class attributes.
    '''

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
        
        if get_value_from_config_file(section_name='DATABASE', value='dialect'):
            self._dialect = get_value_from_config_file(section_name='DATABASE', value='dialect')
        else:
            str_err = "Debe indicar el dialecto de la base de datos en DATABASE -> dialect."
            logger.error(str_err)
            raise Exception(str_err)
        
        if get_value_from_config_file(section_name='DATABASE', value='user'):
            self._user = get_value_from_config_file(section_name='DATABASE', value='user')
        else:
            str_err = "Debe indicar el user de la base de datos en DATABASE -> user."
            logger.error(str_err)
            raise Exception(str_err)
        
        if get_value_from_config_file(section_name='DATABASE', value='pass'):
            self._passwd = get_value_from_config_file(section_name='DATABASE', value='pass')
        else:
            str_err = "Debe indicar el passwd de la base de datos en DATABASE -> passwd."
            logger.error(str_err)
            raise Exception(str_err)
        
        if get_value_from_config_file(section_name='DATABASE', value='ip'):
            self._ip = get_value_from_config_file(section_name='DATABASE', value='ip')
        else:
            str_err = "Debe indicar el ip de la base de datos en DATABASE -> ip."
            logger.error(str_err)
            raise Exception(str_err)
        
        if get_value_from_config_file(section_name='DATABASE', value='port'):
            self._port = get_value_from_config_file(section_name='DATABASE', value='port')
        else:
            str_err = "Debe indicar el port de la base de datos en DATABASE -> port."
            logger.error(str_err)
            raise Exception(str_err)
        
        if get_value_from_config_file(section_name='DATABASE', value='db'):
            self._db = get_value_from_config_file(section_name='DATABASE', value='db')
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