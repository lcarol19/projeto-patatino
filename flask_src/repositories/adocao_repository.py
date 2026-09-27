"""
AdocaoRepository — acesso ao banco referente a adoções e visitas.
"""
from typing import Optional
from repositories.base_repository import BaseRepository
from models.adocao import Adocao


class AdocaoRepository(BaseRepository):

    def buscar_por_id(self, id_adocao: int) -> Optional[Adocao]:
        self._cursor.execute(
            """
            SELECT ad.*,
                   sa.descricao  AS status,
                   a.nome        AS nome_animal,
                   e.descricao   AS especie,
                   t.nome        AS nome_tutor
            FROM adocoes ad
            JOIN status_adocao sa ON sa.id_status  = ad.id_status
            JOIN animais       a  ON a.id_animal   = ad.id_animal
            JOIN especies      e  ON e.id_especie  = a.id_especie
            JOIN tutores       t  ON t.id_tutor    = ad.id_tutor
            WHERE ad.id_adocao = %s
            """,
            (id_adocao,),
        )
        row = self._cursor.fetchone()
        return Adocao.from_dict(row) if row else None

    def inserir(self, adocao: Adocao) -> int:
        """Insere uma nova adoção e retorna o id gerado."""
        self._cursor.execute(
            """
            INSERT INTO adocoes (id_animal, id_tutor, id_status)
            VALUES (%s, %s, %s)
            """,
            (adocao.id_animal, adocao.id_tutor, adocao.id_status),
        )
        return self._cursor.lastrowid

    def marcar_termo_gerado(self, id_adocao: int) -> None:
        self._cursor.execute(
            "UPDATE adocoes SET termo_gerado=TRUE WHERE id_adocao=%s",
            (id_adocao,),
        )
