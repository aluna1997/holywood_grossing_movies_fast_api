import os
import configparser

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi import HTTPException
from typing import Union
from app.logger import configure_log
from fastapi.responses import JSONResponse
from common.globals_common import CONFIG_ROUTE

# Logger.
logger = configure_log()

# OAuth2 Autentication.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_value_from_config_file(section_name: str,value: str) -> Union[str,Exception]:
    '''
    Retrieve a value from a configuration file.

    Parameters:
    - section_name (str): The name of the section in the configuration file.
    - value (str): The name of the value to retrieve within the specified section.

    Returns:
    - str: The value associated with the provided section and name in the configuration file.
           If the section or value is not found, an empty string is returned.

    Raises:
    - Exception: If the configuration file specified by CONFIG_ROUTE does not exist.

    Note:
    - CONFIG_ROUTE is assumed to be a global variable representing the path to the configuration file.
    - The function uses the configparser module to read the configuration file.

    Example:
    ```python
    value = get_value_from_config_file("database", "username")
    ```
    '''
    if not os.path.exists(path=CONFIG_ROUTE):
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


def verify_token(token: str = Depends(oauth2_scheme)) -> Union[str,Exception]:
    '''
    Verify the validity of a provided token against the expected value in the configuration file.

    Parameters:
    - token (str, optional): The authentication token to be verified.
                            Defaults to the result of the `oauth2_scheme` dependency.

    Returns:
    - Union[str, Exception]: If the token is valid, returns the provided token.
                            If the token is invalid or not found in the configuration file,
                            raises an HTTPException with a status code of 401 (Unauthorized)
                            and a corresponding detail message.

    Raises:
    - Exception: If the token is not found in the configuration file.

    Note:
    - This function depends on the `get_value_from_config_file` function to retrieve the expected token value.
    - The configuration file is assumed to have an 'OAUTH' section containing a 'secret_token_api' value.
    - The `oauth2_scheme` is presumed to be a dependency providing the authentication token.

    Example:
    ```python
    verified_token = verify_token("example_token")
    ```
    '''
    if get_value_from_config_file(section_name='OAUTH',value='secret_token_api'):
        if token != get_value_from_config_file(section_name='OAUTH',value='secret_token_api'):
            raise HTTPException(status_code=401, detail="Token inválido")
        return token
    else:
        str_err = 'No existe token en archivo de configuración.'
        logger.error(str_err)
        raise Exception(str_err)

def return_endpoint_response(pyndatic_obj,stataus_code,message,extras = {},ok = True):
    if ok:
        return JSONResponse(content={'message': message, **pyndatic_obj.dict(), **extras}, status_code=stataus_code)
    else:
        raise HTTPException(status_code=stataus_code, detail=message)
    