from datetime import datetime
from http import HTTPStatus

from fastapi import FastAPI

from src.schemas import Message

app = FastAPI()


# Status code define the HTTP response status
# response_model defines the schema of the response body
# (it appears in the OpenAPI documentation: http://localhost:8000/docs)
@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


# Exercise:
# 1. Create a new endpoint that returns the current date and time.
@app.get('/datetime', status_code=HTTPStatus.OK, response_model=Message)
def read_datetime():
    current_datetime = datetime.now().isoformat()
    return {'message': f'O horário atual é: {current_datetime}'}
