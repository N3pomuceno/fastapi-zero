from fastapi import FastAPI

app = FastAPI()


# This is a simple FastAPI application that returns a greeting message.
# It is used to demonstrate the basic structure of a FastAPI application.
# The next line defines a route for the root path ("/") of the application.
# When a GET request is made to this path, it will return a JSON response
# with a message saying "Hello World!".
@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
