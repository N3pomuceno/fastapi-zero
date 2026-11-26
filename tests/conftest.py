from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.app import app
from src.database import get_session
from src.models import User, table_registry
from src.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    # Criamos uma função para retornar nossa
    # fixture de session definida anteriormente.

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    # Substitui a função get_session que usamos para a aplicação real,
    # pela nossa função que retorna a fixture de testes.

    app.dependency_overrides.clear()
    # Limpa a sobrescrita que fizemos no app para usar a fixture de session.


@pytest.fixture
def session():
    # Cria um mecanismo de banco de dados SQLite em memória usando SQLAlchemy.
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    # Cria todas as tabelas no banco de dados de teste antes de
    # cada teste que usa a fixture session.
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        # Fornece uma instância de Session que será injetada em cada teste que
        # solicita a fixture session.
        # Essa sessão será usada para interagir com o banco de dados de teste.
        yield session
    # Após cada teste que usa a fixture session, todas as tabelas do banco
    # de dados de teste são eliminadas, garantindo que cada teste
    # seja executado contra um banco de dados limpo.
    table_registry.metadata.drop_all(engine)
    engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        # Função para alterar o atributo created_at do objeto de target.
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time  # Retorna o datetime na abertura do gerenciamento de contexto.
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session):
    password = 'testtest'
    user = User(
        username='Teste',
        email='teste@test.com',
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Monkey patching para ter o texto puro de password
    user.clean_password = 'testtest'

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
