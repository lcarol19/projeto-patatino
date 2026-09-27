"""
AnimalRepository — todo acesso ao banco referente a animais.
Nenhuma regra de negócio aqui; só SQL.
"""
from typing import List, Optional, Tuple
from repositories.base_repository import BaseRepository
from models.animal import Animal, FotoAnimal


class AnimalRepository(BaseRepository):

    # ── Leitura ──────────────────────────────────────────────

    def buscar_catalogo(
        self,
        especie: str = "",
        porte: str = "",
        sexo: str = "",
        busca: str = "",
        page: int = 1,
        por_pagina: int = 12,
    ) -> Tuple[List[Animal], int]:
        """Retorna (lista de animais, total) para a página do catálogo."""

        filtros = ["a.id_status = 1"]
        params: list = []

        if especie:
            filtros.append("e.descricao = %s")
            params.append(especie)
        if porte:
            filtros.append("p.descricao = %s")
            params.append(porte)
        if sexo:
            filtros.append("a.sexo = %s")
            params.append(sexo)
        if busca:
            filtros.append(
                "(a.nome LIKE %s OR a.temperamento LIKE %s OR a.descricao LIKE %s)"
            )
            like = f"%{busca}%"
            params += [like, like, like]

        where = " AND ".join(filtros)

        self._cursor.execute(
            f"SELECT COUNT(*) AS total FROM animais a "
            f"JOIN especies e ON e.id_especie = a.id_especie "
            f"JOIN portes   p ON p.id_porte   = a.id_porte "
            f"WHERE {where}",
            params,
        )
        total = self._cursor.fetchone()["total"]

        offset = (page - 1) * por_pagina
        self._cursor.execute(
            f"""
            SELECT a.id_animal, a.nome, a.sexo, a.idade_aproximada,
                   a.temperamento, a.descricao,
                   e.descricao AS especie,
                   p.descricao AS porte,
                   COALESCE(MIN(f.url_foto), '') AS foto_url
            FROM animais a
            JOIN especies       e ON e.id_especie = a.id_especie
            JOIN portes         p ON p.id_porte   = a.id_porte
            LEFT JOIN fotos_animais f ON f.id_animal = a.id_animal
            WHERE {where}
            GROUP BY a.id_animal, a.nome, a.sexo, a.idade_aproximada,
                     a.temperamento, a.descricao, e.descricao, p.descricao
            ORDER BY a.data_cadastro DESC
            LIMIT %s OFFSET %s
            """,
            params + [por_pagina, offset],
        )
        rows = self._cursor.fetchall()
        animais = []
        for row in rows:
            a = Animal.from_dict(row)
            if row["foto_url"]:
                a.fotos = [FotoAnimal(
                    id_foto=None,
                    id_animal=a.id_animal,
                    url_foto=row["foto_url"],
                    id_cloudinary=None,
                    ordem=1,
                )]
            animais.append(a)
        return animais, total

    def buscar_por_id(self, id_animal: int) -> Optional[Animal]:
        """Retorna um Animal completo com fotos ou None."""
        self._cursor.execute(
            """
            SELECT a.*, e.descricao AS especie,
                   p.descricao AS porte,
                   s.descricao AS status
            FROM animais a
            JOIN especies      e ON e.id_especie = a.id_especie
            JOIN portes        p ON p.id_porte   = a.id_porte
            JOIN status_animal s ON s.id_status  = a.id_status
            WHERE a.id_animal = %s
            """,
            (id_animal,),
        )
        row = self._cursor.fetchone()
        if not row:
            return None

        animal = Animal.from_dict(row)
        animal.fotos = self._buscar_fotos(id_animal)
        return animal

    def _buscar_fotos(self, id_animal: int) -> List[FotoAnimal]:
        self._cursor.execute(
            "SELECT * FROM fotos_animais WHERE id_animal=%s ORDER BY ordem",
            (id_animal,),
        )
        return [
            FotoAnimal(
                id_foto=r["id_foto"],
                id_animal=r["id_animal"],
                url_foto=r["url_foto"],
                id_cloudinary=r.get("id_cloudinary"),
                ordem=r["ordem"],
                data_cadastro=r.get("data_cadastro"),
            )
            for r in self._cursor.fetchall()
        ]

    def buscar_foto_por_id(self, id_foto: int) -> Optional[FotoAnimal]:
        self._cursor.execute(
            "SELECT * FROM fotos_animais WHERE id_foto=%s", (id_foto,)
        )
        row = self._cursor.fetchone()
        if not row:
            return None
        return FotoAnimal(
            id_foto=row["id_foto"],
            id_animal=row["id_animal"],
            url_foto=row["url_foto"],
            id_cloudinary=row.get("id_cloudinary"),
            ordem=row["ordem"],
        )

    def contar_fotos(self, id_animal: int) -> int:
        self._cursor.execute(
            "SELECT COUNT(*) AS qtd FROM fotos_animais WHERE id_animal=%s",
            (id_animal,),
        )
        return self._cursor.fetchone()["qtd"]

    # ── Escrita ──────────────────────────────────────────────

    def inserir(self, animal: Animal) -> int:
        """Insere um novo animal e retorna o id gerado."""
        self._cursor.execute(
            """
            INSERT INTO animais
                (nome, id_especie, id_porte, id_status, sexo,
                 idade_aproximada, codigo_chip, temperamento,
                 descricao, observacoes)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                animal.nome, animal.id_especie, animal.id_porte,
                animal.id_status, animal.sexo, animal.idade_aproximada,
                animal.codigo_chip, animal.temperamento,
                animal.descricao, animal.observacoes,
            ),
        )
        return self._cursor.lastrowid

    def atualizar(self, animal: Animal) -> None:
        self._cursor.execute(
            """
            UPDATE animais SET
                nome=%s, id_especie=%s, id_porte=%s, id_status=%s,
                sexo=%s, idade_aproximada=%s, codigo_chip=%s,
                temperamento=%s, descricao=%s, observacoes=%s
            WHERE id_animal=%s
            """,
            (
                animal.nome, animal.id_especie, animal.id_porte,
                animal.id_status, animal.sexo, animal.idade_aproximada,
                animal.codigo_chip, animal.temperamento,
                animal.descricao, animal.observacoes,
                animal.id_animal,
            ),
        )

    def excluir(self, id_animal: int) -> None:
        self._cursor.execute(
            "DELETE FROM animais WHERE id_animal=%s", (id_animal,)
        )

    def inserir_foto(self, foto: FotoAnimal) -> int:
        self._cursor.execute(
            """
            INSERT INTO fotos_animais
                (id_animal, url_foto, id_cloudinary, ordem)
            VALUES (%s,%s,%s,%s)
            """,
            (foto.id_animal, foto.url_foto, foto.id_cloudinary, foto.ordem),
        )
        return self._cursor.lastrowid

    def excluir_foto(self, id_foto: int) -> None:
        self._cursor.execute(
            "DELETE FROM fotos_animais WHERE id_foto=%s", (id_foto,)
        )

    # ── Domínios ─────────────────────────────────────────────

    def buscar_id_especie(self, descricao: str) -> int:
        self._cursor.execute(
            "SELECT id_especie FROM especies WHERE descricao=%s", (descricao,)
        )
        return self._cursor.fetchone()["id_especie"]

    def buscar_id_porte(self, descricao: str) -> int:
        self._cursor.execute(
            "SELECT id_porte FROM portes WHERE descricao=%s", (descricao,)
        )
        return self._cursor.fetchone()["id_porte"]

    def buscar_id_status(self, descricao: str) -> int:
        self._cursor.execute(
            "SELECT id_status FROM status_animal WHERE descricao=%s", (descricao,)
        )
        return self._cursor.fetchone()["id_status"]
