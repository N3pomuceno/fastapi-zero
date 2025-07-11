from http import HTTPStatus

from fastapi.testclient import TestClient

from src.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


# Exercise:
# 1. Create a new endpoint that returns the current date and time.
def test_datetime_deve_retornar_ok_e_data_hora_atual():
    client = TestClient(app)  # Arrange

    response = client.get('/datetime')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert 'message' in response.json()
    assert 'O horário atual é:' in response.json()['message']
