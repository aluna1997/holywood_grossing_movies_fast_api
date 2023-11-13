from fastapi import FastAPI
from app.routes import sponsor_route
from app.routes import highest_holywood_grossing_movie_route

app = FastAPI()

# Routes.
app.include_router(sponsor_route.router)
app.include_router(highest_holywood_grossing_movie_route.router)

@app.get('/')
def healthy():
    '''
    Endpoint that is responsible for providing a message that the application is 
    running correctly.
    
    Returns:
        str: Always returns "healthy".
    '''
    return "healthy"