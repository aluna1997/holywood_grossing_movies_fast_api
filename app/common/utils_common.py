import os

import configparser

from app.logger import configure_log
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

# Logger.
logger = configure_log()

# Globals.
CONFIG_ROUTE = '../app/config/cfg.cfg'

# OAuth2 Autentication.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_value_from_config_file(section_name: str,value: str) -> str:
    if not os.path.exists(CONFIG_ROUTE):
        str_err = f'No existe archivo de configuracion: {CONFIG_ROUTE}.'
        logger.error(str_err)
        raise Exception(str_err)
    
    config = configparser.ConfigParser()
    config.read(CONFIG_ROUTE)
    
    if config.has_option(section_name, value):
            return config.get(section_name, value)
    else:
        str_err = f'Debe indicar un {section_name} válido.'
        logger.error(str_err)
        return ''


def verify_token(token: str = Depends(oauth2_scheme)):

    if get_value_from_config_file(section_name='OAUTH',value='secret_token_api'):
        if token != get_value_from_config_file(section_name='OAUTH',value='secret_token_api'):
            raise HTTPException(status_code=401, detail="Token inválido")
        return token
    else:
        str_err = 'No existe token en archivo de configuración.'
        logger.error(str_err)
        raise Exception(str_err)
