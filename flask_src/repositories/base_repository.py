"""
BaseRepository — classe base para todos os repositories.
Centraliza a abertura/fechamento da conexão com o banco.
"""
from db import conectar


class BaseRepository:
    """Abre uma conexão ao ser instanciado e a fecha ao sair do bloco `with`."""

    def __init__(self):
        self._conn = conectar()
        if not self._conn:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        self._cursor = self._conn.cursor(dictionary=True)

    # ── Context manager: permite usar `with AnimalRepository() as repo:`
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self._conn.rollback()
        else:
            self._conn.commit()
        self._cursor.close()
        self._conn.close()

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()
