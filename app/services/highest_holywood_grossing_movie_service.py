from app.services.db_connection_service import DatabaseConnection
from app.model.sponsor_model import Sponsor
from app.model.highest_holywood_grossing_movie_model import HighestHolywoodGrossingMovie
from datetime import datetime
from app.logger import configure_log

# Typing
from typing import Dict
from typing import Union
from typing import List
from sqlalchemy.orm import Session

# Globals.
logger = configure_log()
optionals: list = ['id_movie','creation_date','active']

def create_highest_holywood_grossing_movie(session: Session,info_movie: Dict) -> Union[int,Exception]:
    '''
    Create a new entry for the Highest Hollywood Grossing Movie.

    This function creates a new record in the database for the Highest Hollywood Grossing Movie based on the provided information.

    :param session: SQLAlchemy session object.
    :type session: Session

    :param info_movie: A dictionary containing information about the movie.
    :type info_movie: dict

    :return: The ID of the newly created movie entry.
    :rtype: int

    :raises: Exception if there is an error during the creation process.

    Example:
    >>> info = {'title': 'Avatar', 'box_office': 2787965087, 'release_year': 2009}
    >>> create_highest_hollywood_grossing_movie(session, info)
    1
    '''
    new_movie = HighestHolywoodGrossingMovie()

    for key,value in info_movie.items():
        if (not value) and (key not in optionals):
            str_err = f'{key} no puede ser vacío al crear un nuevo highest_holywood_grossing_movie.'
            logger.error(str_err)
            raise Exception(str_err)
        else:
            setattr(new_movie, key, value)
        
    try:
        session.add(new_movie)
        session.commit()
        return new_movie.id_movie
    except Exception as err:
        session.rollback()
        str_err = f'Ocurrió un error al crear HighestHolywoodGrossingMovie: {str(err)}.'
        logger.error(str_err)
        raise err
    
def read_highest_holywood_grossing_movie(session: Session,id_movie: int = False) -> Union[List[HighestHolywoodGrossingMovie], HighestHolywoodGrossingMovie, Exception]:
    '''
    Retrieve Highest Hollywood Grossing Movies from the database.

    This function retrieves Highest Hollywood Grossing Movies from the database based on the provided ID or all active movies.

    :param session: SQLAlchemy session object.
    :type session: Session

    :param id_movie: An optional ID of the movie to retrieve. If not provided, all active movies are retrieved.
    :type id_movie: int, optional

    :return: A list of Highest Hollywood Grossing Movies matching the query criteria.
    :rtype: list

    :raises: Exception if there is an error during the retrieval process.

    Example:
    >>> # Retrieve all active movies
    >>> read_highest_hollywood_grossing_movie(session)

    >>> # Retrieve a specific movie by ID
    >>> read_highest_hollywood_grossing_movie(session, 1)
    '''

    if not id_movie:
        try:
            filter = HighestHolywoodGrossingMovie.active == 1
            movies = session.query(HighestHolywoodGrossingMovie).filter(filter).all()
        except Exception as err:
            session.rollback()
            str_err = f'Ocurrió un error al leer HighestHolywoodGrossingMovie: {str(err)}.'
            logger.error(str_err)
            raise err
    else:
        try:
            movies = session.get(HighestHolywoodGrossingMovie,id_movie)
        except Exception as err:
            session.rollback()
            str_err = f'Ocurrió un error al leer HighestHolywoodGrossingMovie: {str(err)}.'
            logger.error(str_err)
            raise err

    return movies

def update_highest_holywood_grossing_movie(session: Session,id_movie: int,info_movie: Dict) -> Union[int, Exception]:
    '''
    Update an existing Highest Hollywood Grossing Movie in the database.

    This function updates an existing Highest Hollywood Grossing Movie in the database based on the provided ID and information.

    :param session: SQLAlchemy session object.
    :type session: Session

    :param id_movie: The ID of the movie to be updated.
    :type id_movie: int

    :param info_movie: A dictionary containing updated information for the movie.
    :type info_movie: dict

    :return: The ID of the updated movie.
    :rtype: int

    :raises: Exception if there is an error during the update process.

    Example:
    >>> info = {'title': 'Updated Movie', 'box_office': 300000000, 'release_year': 2022}
    >>> update_highest_hollywood_grossing_movie(session, 1, info)
    '''

    if not id_movie:
        str_err = 'Para actualizar, el id_movie no debe ser vacío.'
        logger.error(str_err)
        raise Exception(str_err)
    
    movie = session.get(HighestHolywoodGrossingMovie,id_movie)

    if not movie:
        str_err = 'El id a actualizar no existe, no se actualiza nada.'
        logger.error(str_err)
        raise Exception(str_err)

    for key,value in info_movie.items():
        if getattr(movie, key, None):
            setattr(movie, key, value)
        else:
            logger.warning(f'El atributo {key} no existe para el objeto de highest_holywood_grossing_movie, se ignora.')

    try:
        session.add(movie)
        session.commit()
        return movie.id_movie
    except Exception as err:
        session.rollback()
        str_err = f'Ocurrió un error al actualizar HighestHolywoodGrossingMovie: {str(err)}.'
        logger.error(str_err)
        raise err

def delete_highest_holywood_grossing_movie(session: Session,id_movie: int) -> [int, Exception]:
    '''
    Delete a Highest Hollywood Grossing Movie from the database.

    This function marks a Highest Hollywood Grossing Movie as inactive in the database based on the provided ID.

    :param session: SQLAlchemy session object.
    :type session: Session

    :param id_movie: The ID of the movie to be deleted.
    :type id_movie: int

    :return: The ID of the movie that was marked as inactive.
    :rtype: int

    :raises: Exception if there is an error during the deletion process.

    Example:
    >>> delete_highest_hollywood_grossing_movie(session, 1)
    '''
    if not id_movie:
        str_err = 'Para eliminar, el id_movie no debe ser vacío.'
        logger.error(str_err)
        raise Exception(str_err)
    
    movie = session.get(HighestHolywoodGrossingMovie,id_movie)

    if not movie:
        logger.warning('El id a eliminar no existe, no se actualiza nada.')

    try:
        movie.active = 0
        session.commit()
        return movie.id_movie
    except Exception as err:
        session.rollback()
        str_err = f'Ocurrió un error al eliminar HighestHolywoodGrossingMovie: {str(err)}.'
        logger.error(str_err)
        raise err