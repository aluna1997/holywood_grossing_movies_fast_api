from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def healthy():
    '''
    Endpoint that is responsible for providing a message that the application is 
    running correctly.
    
    Returns:
        str: Always returns "healthy".
    '''
    return "healthy"

@app.get('/movie/{id_movie}')
def get_movie(id_movie: int):
    '''
    Endpoint that is responsible for obtaining information about a movie with a 
    specific id given by the user.

    Args:
        id_movie (int): ID of te movie to search in te DB.

    Returns:
        bool: The return value. True for success, False otherwise.

    Note: 

    Examples:
    '''

    pass

if __name__ == "__main__":
    from app.model.db_connection import DatabaseConnection
    from app.model.pydantic_sqlalchemy.sponsor import Sponsor
    from app.model.pydantic_sqlalchemy.highest_holywood_grossing_movie import HighestHolywoodGrossingMovie
    
    
    db_conn = DatabaseConnection()
    session = db_conn.get_session()
    sponsors = session.query(Sponsor).all()
    for s in sponsors:
        print(s.active)