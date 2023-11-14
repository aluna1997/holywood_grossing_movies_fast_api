from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.routing import APIRouter

from app.logger import configure_log
from app.common.utils_common import get_value_from_config_file
from app.common.utils_common import verify_token
from app.services.highest_holywood_grossing_movie_service import create_highest_holywood_grossing_movie
from app.model.db_connection_object_model import DatabaseConnection
from app.common.globals_common import HTTP_CREATED

# Pyndatic Models
from app.model.highest_holywood_grossing_movie_model import PydanticHighestHolywoodGrossingMovie

# Logger.
logger = configure_log()

# OAuth2 Autentication.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Router from API.
router = APIRouter(prefix='/v1')

@router.post("/highest_holywood_grossing_movie")
def create_highest_holywood_grossing_movie_endpoint(token: str = Depends(verify_token), pydantic_highest_holywood_grossing_movie: PydanticHighestHolywoodGrossingMovie = None):
    db_connection = DatabaseConnection()
    session = db_connection.get_session()
    movie_info = pydantic_highest_holywood_grossing_movie.dict()
    id_movie = create_highest_holywood_grossing_movie(session=session,movie_info=movie_info)
    db_connection.close_session()
    
