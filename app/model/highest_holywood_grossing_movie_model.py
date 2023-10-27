from app.model.db_connection import DatabaseConnection
from app.model.pydantic_sqlalchemy.sponsor import Sponsor
from app.model.pydantic_sqlalchemy.highest_holywood_grossing_movie import HighestHolywoodGrossingMovie

from datetime import datetime

# Logger.
from app.logger import configure_log
logger = configure_log()

# GLOBALS
optionals = ['creation_date','active']

def create_highest_holywood_grossing_movie(session,info_movie):
    '''
    
    '''
    new_movie = HighestHolywoodGrossingMovie()

    for key,value in info_movie.items():
        if (not value) and (key not in optionals):
            str_err = '{key} no puede ser vacío al crear un nuevo highest_holywood_grossing_movie.'
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
        str_err = f'Ocurrió un error al actualizar HighestHolywoodGrossingMovie: {str(err)}.'
        logger.error(str_err)
        raise err
    
def read_highest_holywood_grossing_movie(session,id_movie = False):
    
    if not id_movie:
        movies = session.query(HighestHolywoodGrossingMovie).all()
    else:
        movies = session.query(HighestHolywoodGrossingMovie).get(id_movie)

    return movies

def update_highest_holywood_grossing_movie(session,id_movie,info_movie):

    if not id_movie:
        str_err = 'Para actualizar, el id_movie no debe ser vacío.'
        logger.error(str_err)
        raise Exception(str_err)
    
    movie = session.query(HighestHolywoodGrossingMovie).get(id_movie)

    if not movie:
        logger.warning('El id a actualizar no existe, no se actualiza nada.')

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
    

if __name__ == "__main__":
    db_conn = DatabaseConnection()
    session = db_conn.get_session()


    info_movie_1 = {'title': 'Up 2: una aventura de altura 2',
                  'movie_info': 'Up is a 2009 American animated comedy-drama adventure film produced by Pixar Animation Studios and released by Walt Disney Pictures.',
                  'distributor': 'Walt Disney Studios Motion Pictures',
                  'release_date': 'May 13, 2009',
                  'domestic_sales': 1000000,
                  'international_sales': 2000000,
                  'world_sales': 3000000,
                  'genere': "['Action', 'Adventure', 'Fantasy', 'Sci-Fi']",
                  'movie_runtime': '2hr 12 min',
                  'license': 'NA',
                  'creation_date': datetime.now(),
                  'active': 1}
    
    info_movie_3 = {'title': 'Up 3: una aventura de altura 3',
                  'movie_info': 'Up is a 2009 American animated comedy-drama adventure film produced by Pixar Animation Studios and released by Walt Disney Pictures.',
                  'distributor': 'Walt Disney Studios Motion Pictures',
                  'release_date': 'May 13, 2009',
                  'domestic_sales': 1000000,
                  'international_sales': 2000000,
                  'world_sales': 3000000,
                  'genere': "['Action', 'Adventure', 'Fantasy', 'Sci-Fi']",
                  'movie_runtime': '2hr 12 min',
                  'license': 'NA'}

    #last_id = create_highest_holywood_grossing_movie(session,info_movie_1)
    #print(last_id)


    movie = read_highest_holywood_grossing_movie(session,id_movie=3)
    print(movie.__dict__)
    db_conn.close_session()