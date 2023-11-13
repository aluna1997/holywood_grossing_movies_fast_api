from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.routing import APIRouter
from app.logger import configure_log
from app.common.utils_common import get_value_from_config_file
from app.common.utils_common import verify_token

# Pyndatic Models
from app.model.highest_holywood_grossing_movie_model import PydanticHighestHolywoodGrossingMovie

# Globals.
logger = configure_log()

# OAuth2 Autentication.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Router from API.
router = APIRouter(prefix='/v1')

@router.post("/highest_holywood_grossing_movie")
def create_highest_holywood_grossing_movie_endpoint(token: str = Depends(verify_token), pydantic_highest_holywood_grossing_movie: PydanticHighestHolywoodGrossingMovie = None):
    logger.debug(pydantic_highest_holywood_grossing_movie.__dict__)
    return pydantic_highest_holywood_grossing_movie