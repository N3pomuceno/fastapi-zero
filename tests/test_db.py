from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import User


def test_create_user(session: Session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice', password='secret', email='alice@example.com'
        )
        # O método .add da sessão, adiciona o registro a sessão.
        # O dado fica em um estado transiente.
        # Ele não foi adicionado ao banco de dados ainda.
        # Mas já está reservado na sessão.
        session.add(new_user)
        # O método .commit persiste todas as alterações
        # pendentes na sessão ao banco de dados.
        # Ou seja, ele salva o novo usuário no banco de dados.
        session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'alice@example.com',
        'created_at': time,
    }
