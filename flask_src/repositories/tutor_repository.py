"""
TutorRepository — acesso ao banco referente a tutores.
"""
from typing import Optional
from repositories.base_repository import BaseRepository
from models.tutor import Tutor


class TutorRepository(BaseRepository):

    def buscar_por_id(self, id_tutor: int) -> Optional[Tutor]:
        self._cursor.execute(
            """
            SELECT t.*, tm.descricao AS tipo_moradia
            FROM tutores t
            LEFT JOIN tipos_moradia tm ON tm.id_tipo = t.id_tipo_moradia
            WHERE t.id_tutor = %s
            """,
            (id_tutor,),
        )
        row = self._cursor.fetchone()
        return Tutor.from_dict(row) if row else None

    def buscar_id_tipo_moradia(self, descricao: str) -> Optional[int]:
        self._cursor.execute(
            "SELECT id_tipo FROM tipos_moradia WHERE descricao=%s", (descricao,)
        )
        row = self._cursor.fetchone()
        return row["id_tipo"] if row else None

    def inserir(self, tutor: Tutor) -> int:
        """Insere um novo tutor e retorna o id gerado."""
        self._cursor.execute(
            """
            INSERT INTO tutores
                (nome, rg, cpf, cep, endereco, numero, complemento,
                 bairro, cidade, estado, telefone, email,
                 horas_fora_casa, id_tipo_moradia, casa_telada,
                 acesso_quintal, acesso_rua,
                 autoriza_visita_ong, autoriza_foto_mural, observacoes)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                tutor.nome, tutor.rg, tutor.cpf,
                tutor.cep, tutor.endereco, tutor.numero,
                tutor.complemento, tutor.bairro, tutor.cidade,
                tutor.estado, tutor.telefone, tutor.email,
                tutor.horas_fora_casa, tutor.id_tipo_moradia,
                tutor.casa_telada, tutor.acesso_quintal,
                tutor.acesso_rua, tutor.autoriza_visita_ong,
                tutor.autoriza_foto_mural, tutor.observacoes,
            ),
        )
        return self._cursor.lastrowid
