from app.model.db_connection import DatabaseConnection
from app.model.pydantic_sqlalchemy.sponsor import Sponsor
from app.model.pydantic_sqlalchemy.highest_holywood_grossing_movie import HighestHolywoodGrossingMovie

from datetime import datetime

# Logger.
from app.logger import configure_log
logger = configure_log()

def create_highest_holywood_grossing_movie(session,info_movie):
    '''
    
    '''
    new_movie = HighestHolywoodGrossingMovie()

    for key,value in info_movie.items():
        optionals = ['creation_date','active']
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

    last_id = create_highest_holywood_grossing_movie(session,info_movie_3)
    print(last_id)
    db_conn.close_session()