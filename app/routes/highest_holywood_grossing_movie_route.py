from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.routing import APIRouter

from app.logger import configure_log
from app.common.utils_common import get_value_from_config_file
from app.common.utils_common import verify_token
from app.common.globals_common import HTTP_CREATED
from app.common.globals_common import INTERNAL_SERVER_ERROR
from app.common.globals_common import ERR_MSG
from app.common.globals_common import HTTP_OK
from app.common.globals_common import DELETE_OK
from app.common.utils_common import return_endpoint_response

from app.model.db_connection_object_model import DatabaseConnection
from app.model.highest_holywood_grossing_movie_model import PydanticHighestHolywoodGrossingMovie

from app.services.highest_holywood_grossing_movie_service import create_highest_holywood_grossing_movie
from app.services.highest_holywood_grossing_movie_service import read_highest_holywood_grossing_movie
from app.services.highest_holywood_grossing_movie_service import update_highest_holywood_grossing_movie
from app.services.highest_holywood_grossing_movie_service import delete_highest_holywood_grossing_movie

from typing import Dict
from typing import Union
from typing import List
from typing import Optional

# Logger.
logger = configure_log()

# OAuth2 Autentication.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Router from API.
router = APIRouter(prefix='/v1')

@router.post("/highest_holywood_grossing_movie")
def create_highest_holywood_grossing_movie_endpoint(token: str = Depends(verify_token), pydantic_highest_holywood_grossing_movie: PydanticHighestHolywoodGrossingMovie = None) -> Dict:
    
    try:
        db_connection = DatabaseConnection()
        session = db_connection.get_session()
    except Exception as err:
        logger.error(f'Ocurrió un error al crear la sessión a la BD: {str(err)}.')
        return return_endpoint_response(stataus_code=INTERNAL_SERVER_ERROR,message=ERR_MSG,ok=False)
    
    try:
        id_movie = create_highest_holywood_grossing_movie(session=session,info_movie=pydantic_highest_holywood_grossing_movie.dict())
        return return_endpoint_response( objs=[pydantic_highest_holywood_grossing_movie],
                                         stataus_code=HTTP_CREATED,
                                         message='Se creo el objeto con éxito.',
                                         extras={'id_movie':id_movie} )
    except Exception as err:
        logger.error(f'Ocurrió un error al crear el recurso en la BD: {str(err)}.')
        return return_endpoint_response(stataus_code=INTERNAL_SERVER_ERROR,message=ERR_MSG,ok=False)
    
    try:
        db_connection.close_session()
    except Exception as err:
        logger.error(f'Ocurrió un error al cerrar la sessión a la BD: {str(err)}.')
        return return_endpoint_response(stataus_code=INTERNAL_SERVER_ERROR,message=ERR_MSG,ok=False)
    

@router.get("/highest_holywood_grossing_movie/")
def read_highest_holywood_grossing_movie_endpoint(token: str = Depends(verify_token), id_movie: Optional[int] = None) -> Dict:
    try:
        db_connection = DatabaseConnection()
        session = db_connection.get_session()
    except Exception as err:
        logger.error(f'Ocurrió un error al crear la sessión a la BD: {str(err)}.')
        return return_endpoint_response(stataus_code=INTERNAL_SERVER_ERROR,message=ERR_MSG,ok=False)
    
    try:
        highest_holywood_grossing_movie = read_highest_holywood_grossing_movie(session=session,id_movie=id_movie)
        return return_endpoint_response( objs=highest_holywood_grossing_movie,
                                         stataus_code=HTTP_OK,
                                         message='Se obtuvo el objeto con éxito.',
                                         extras={'id_movie':id_movie} if id_movie else {} )
    except Exception as err:
        logger.error(f'Ocurrió un error al obtener el recurso en la BD: {str(err)}.')
        return return_endpoint_response(stataus_code=INTERNAL_SERVER_ERROR,message=ERR_MSG,ok=False)
    
    try:
        db_connection.close_session()
    except Exception as err:
        logger.error(f'Ocurrió un error al cerrar la sessión a la BD: {str(err)}.')
        return return_endpoint_response(stataus_code=INTERNAL_SERVER_ERROR,message=ERR_MSG,ok=False)
    
@router.patch("/highest_holywood_grossing_movie/{id_movie}")
def update_highest_holywood_grossing_movie_endpoint(token: str = Depends(verify_token), id_movie: int = 0, pydantic_highest_holywood_grossing_movie: PydanticHighestHolywoodGrossingMovie = None) -> Dict:
    try:
        db_connection = DatabaseConnection()
        session = db_connection.get_session()
    except Exception as err:
        logger.error(f'Ocurrió un error al crear la sessión a la BD: {str(err)}.')
        return return_endpoint_response(stataus_code=INTERNAL_SERVER_ERROR,message=ERR_MSG,ok=False)
    
    try:
        id_movie = update_highest_holywood_grossing_movie(session=session,id_movie=id_movie,info_movie=pydantic_highest_holywood_grossing_movie.dict())
        return return_endpoint_response( stataus_code=HTTP_OK,
                                         message='Se actualizó el objeto con éxito.',
                                         extras={'id_movie':id_movie} if id_movie else {} )
    except Exception as err:
        logger.error(f'Ocurrió un error al actualizar el recurso en la BD: {str(err)}.')
        return return_endpoint_response(stataus_code=INTERNAL_SERVER_ERROR,message=ERR_MSG,ok=False)
    
    try:
        db_connection.close_session()
    except Exception as err:
        logger.error(f'Ocurrió un error al cerrar la sessión a la BD: {str(err)}.')
        return return_endpoint_response(stataus_code=INTERNAL_SERVER_ERROR,message=ERR_MSG,ok=False)
    
@router.delete("/highest_holywood_grossing_movie/{id_movie}")
def delete_highest_holywood_grossing_movie_endpoint(token: str = Depends(verify_token), id_movie: int = 0) -> Dict:
    try:
        db_connection = DatabaseConnection()
        session = db_connection.get_session()
    except Exception as err:
        logger.error(f'Ocurrió un error al crear la sessión a la BD: {str(err)}.')
        return return_endpoint_response(stataus_code=INTERNAL_SERVER_ERROR,message=ERR_MSG,ok=False)
    
    try:
        id_movie = delete_highest_holywood_grossing_movie(session=session,id_movie=id_movie)
        return return_endpoint_response(stataus_code=DELETE_OK)
    except Exception as err:
        logger.error(f'Ocurrió un error al eliminar el recurso en la BD: {str(err)}.')
        return return_endpoint_response(stataus_code=INTERNAL_SERVER_ERROR,message=ERR_MSG,ok=False)
    
    try:
        db_connection.close_session()
    except Exception as err:
        logger.error(f'Ocurrió un error al cerrar la sessión a la BD: {str(err)}.')
        return return_endpoint_response(stataus_code=INTERNAL_SERVER_ERROR,message=ERR_MSG,ok=False)
    
