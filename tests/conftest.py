from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from src.app import app
from src.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    # Cria um mecanismo de banco de dados SQLite em memória usando SQLAlchemy.
    engine = create_engine('sqlite:///:memory:')
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


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        # Função para alterar o atributo created_at do objeto de target.
        if hasattr(target, 'created_at'):
            target.created_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time  # Retorna o datetime na abertura do gerenciamento de contexto.
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
