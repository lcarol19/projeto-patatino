"""
AnimalService — regras de negócio referentes a animais.
Orquestra repositórios e serviços externos (Cloudinary).
"""
from typing import List, Tuple, Optional
from models.animal import Animal, FotoAnimal
from repositories.animal_repository import AnimalRepository
from services.imagem_service import ImagemService


class AnimalService:

    MAX_FOTOS = 3

    def __init__(self):
        self._imagem_service = ImagemService()

    # ── Consultas ────────────────────────────────────────────

    def listar_catalogo(
        self,
        especie: str = "",
        porte: str = "",
        sexo: str = "",
        busca: str = "",
        page: int = 1,
    ) -> Tuple[List[Animal], int, int]:
        """Retorna (animais, total, total_paginas) para o catálogo."""
        por_pagina = 12
        with AnimalRepository() as repo:
            animais, total = repo.buscar_catalogo(
                especie=especie, porte=porte, sexo=sexo,
                busca=busca, page=page, por_pagina=por_pagina,
            )
        total_paginas = max(1, (total + por_pagina - 1) // por_pagina)
        return animais, total, total_paginas

    def buscar_por_id(self, id_animal: int) -> Optional[Animal]:
        with AnimalRepository() as repo:
            return repo.buscar_por_id(id_animal)

    # ── Cadastro ─────────────────────────────────────────────

    def cadastrar(self, form: dict, arquivos: list) -> int:
        """
        Cria um novo animal com suas fotos.
        Retorna o id do animal criado.
        Lança ValueError se dados obrigatórios faltarem.
        """
        self._validar_form_animal(form)

        with AnimalRepository() as repo:
            id_especie = repo.buscar_id_especie(form["especie"])
            id_porte   = repo.buscar_id_porte(form["porte"])

            animal = Animal(
                id_animal=None,
                nome=form["nome"].strip(),
                id_especie=id_especie,
                id_porte=id_porte,
                sexo=form.get("sexo", "Não informado"),
                idade_aproximada=int(form["idade_aproximada"])
                    if form.get("idade_aproximada") else None,
                codigo_chip=form.get("codigo_chip") or None,
                temperamento=form.get("temperamento") or None,
                descricao=form.get("descricao") or None,
                observacoes=form.get("observacoes") or None,
            )
            id_animal = repo.inserir(animal)

            fotos_salvas = self._salvar_fotos(repo, id_animal, arquivos)

        return id_animal

    # ── Edição ───────────────────────────────────────────────

    def atualizar(self, id_animal: int, form: dict,
                  arquivos: list, fotos_remover: list) -> None:
        self._validar_form_animal(form)

        with AnimalRepository() as repo:
            id_especie = repo.buscar_id_especie(form["especie"])
            id_porte   = repo.buscar_id_porte(form["porte"])
            id_status  = repo.buscar_id_status(form["status"])

            animal = Animal(
                id_animal=id_animal,
                nome=form["nome"].strip(),
                id_especie=id_especie,
                id_porte=id_porte,
                id_status=id_status,
                sexo=form.get("sexo", "Não informado"),
                idade_aproximada=int(form["idade_aproximada"])
                    if form.get("idade_aproximada") else None,
                codigo_chip=form.get("codigo_chip") or None,
                temperamento=form.get("temperamento") or None,
                descricao=form.get("descricao") or None,
                observacoes=form.get("observacoes") or None,
            )
            repo.atualizar(animal)

            # remove fotos marcadas
            for id_foto in fotos_remover:
                foto = repo.buscar_foto_por_id(int(id_foto))
                if foto and foto.id_cloudinary:
                    self._imagem_service.excluir(foto.id_cloudinary)
                repo.excluir_foto(int(id_foto))

            # adiciona novas fotos respeitando o limite
            qtd_atual = repo.contar_fotos(id_animal)
            vagas = max(0, self.MAX_FOTOS - qtd_atual)
            self._salvar_fotos(repo, id_animal, arquivos[:vagas])

    # ── Exclusão ─────────────────────────────────────────────

    def excluir(self, id_animal: int) -> None:
        with AnimalRepository() as repo:
            animal = repo.buscar_por_id(id_animal)
            if animal:
                for foto in animal.fotos:
                    if foto.id_cloudinary:
                        self._imagem_service.excluir(foto.id_cloudinary)
            repo.excluir(id_animal)

    # ── Helpers privados ─────────────────────────────────────

    def _validar_form_animal(self, form: dict) -> None:
        if not form.get("nome", "").strip():
            raise ValueError("O nome do animal é obrigatório.")
        if not form.get("especie"):
            raise ValueError("A espécie é obrigatória.")
        if not form.get("porte"):
            raise ValueError("O porte é obrigatório.")

    def _salvar_fotos(
        self, repo: AnimalRepository, id_animal: int, arquivos: list
    ) -> list:
        """Faz upload das fotos e persiste no banco. Retorna public_ids salvos."""
        public_ids = []
        qtd_atual = repo.contar_fotos(id_animal)
        for i, arquivo in enumerate(arquivos, start=1):
            if not arquivo or not arquivo.filename:
                continue
            url, public_id = self._imagem_service.upload(
                arquivo, pasta="patatino/animais"
            )
            if url:
                public_ids.append(public_id)
                repo.inserir_foto(FotoAnimal(
                    id_foto=None,
                    id_animal=id_animal,
                    url_foto=url,
                    id_cloudinary=public_id,
                    ordem=qtd_atual + i,
                ))
        return public_ids
