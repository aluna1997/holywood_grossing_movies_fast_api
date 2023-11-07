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