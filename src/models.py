from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

# Cada classe que é registrada pelo objeto registry é
# automaticamente mapeada para uma tabela no banco de dados.
# Adicionalmente, a classe base inclui um objeto de metadados
# que é uma coleção de todas as tabelas declaradas.
# Este objeto é utilizado para gerenciar operações como criação,
# modificação e exclusão de tabelas.
table_registry = registry()


# Vamos usar o registrador de tabelas, que já faz a
# conversão automática das classes em dataclasses
@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
