from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, text
from sqlalchemy.orm import relationship
from app.model.base_model import Base
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from app.logger import configure_log
from typing import Optional
from datetime import datetime
from pydantic import validator

# Globals.
logger = configure_log()


# SqlAlchemy Class.
class HighestHolywoodGrossingMovie(Base):
    '''
    Represents a model for the highest Hollywood grossing movie in a database.

    This class defines the structure of the "highest_hollywood_grossing_movie" table,
    including its columns, relationships, and default values.

    Attributes:
        id_movie (int): The primary key for the movie record.
        title (str): The title of the movie.
        movie_info (str): Information about the movie.
        distributor (str): The distributor of the movie.
        release_date (str): The release date of the movie.
        domestic_sales (int): The domestic sales of the movie.
        international_sales (int): The international sales of the movie.
        world_sales (int): The worldwide sales of the movie.
        genre (str): The genre of the movie.
        movie_runtime (str): The runtime of the movie.
        license (str): The license associated with the movie.
        creation_date (datetime): The timestamp of when the record was created.
        active (int): Flag indicating the status of the movie record (default is 1, which means active).

    Relationships:
        sponsors (relationship): A relationship to the "Sponsor" model, indicating sponsors associated with the movie.
    '''
    __tablename__ = "highest_holywood_grossing_movie"

    id_movie = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    movie_info = Column(String, nullable=False)
    distributor = Column(String, nullable=False)
    release_date = Column(String, nullable=False)
    domestic_sales = Column(Integer, nullable=False)
    international_sales = Column(Integer, nullable=False)
    world_sales = Column(Integer, nullable=False)
    genere = Column(String, nullable=False)
    movie_runtime = Column(String, nullable=False)
    license = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    active = Column(SmallInteger, nullable=False, default=1)

    # Relations.
    sponsors = relationship('Sponsor', back_populates='movie', cascade='all, delete, delete-orphan')

# Pydantic Class.
PydanticHighestHolywoodGrossingMovieAux = sqlalchemy_to_pydantic(HighestHolywoodGrossingMovie, exclude=['sponsors'])

class PydanticHighestHolywoodGrossingMovie(PydanticHighestHolywoodGrossingMovieAux):
    # Making the email attribute optional.
    id_movie: Optional[int]
    creation_date: Optional[datetime]
    active: Optional[int]
    
    @validator('title')
    def validate_title_length(cls, value):
        logger.debug('entre')
        logger.debug(value)
        logger.debug(type(value))
        if value and len(value) != 5:
            raise ValueError("Title must be at least 5 characters long")
        return value