from fastapi import APIRouter
from app.logger import configure_log

# Pyndatic Models
from app.model.highest_holywood_grossing_movie_model import PydanticHighestHolywoodGrossingMovie

# Globals.
logger = configure_log()

router = APIRouter(prefix='/v1')

@router.post("/highest_holywood_grossing_movie")
def create_highest_holywood_grossing_movie_endpoint(pydantic_highest_holywood_grossing_movie: PydanticHighestHolywoodGrossingMovie):
    logger.debug(pydantic_highest_holywood_grossing_movie.__dict__)
    return pydantic_highest_holywood_grossing_movie