"""
AdocaoService — regras de negócio do processo de adoção.
"""
from typing import Optional
from models.adocao import Adocao
from models.tutor import Tutor
from repositories.adocao_repository import AdocaoRepository
from repositories.tutor_repository import TutorRepository
from repositories.animal_repository import AnimalRepository


class AdocaoService:

    def solicitar(self, id_animal: int, form: dict) -> int:
        """
        Cria tutor + adoção a partir do formulário.
        Valida disponibilidade do animal antes de prosseguir.
        Retorna o id_adocao criado.
        """
        self._validar_animal_disponivel(id_animal)
        self._validar_form_tutor(form)

        cpf_limpo = (form["cpf"]
                     .replace(".", "")
                     .replace("-", "")
                     .strip())

        with TutorRepository() as tutor_repo:
            id_tipo_moradia = tutor_repo.buscar_id_tipo_moradia(
                form.get("tipo_moradia", "")
            )

            tutor = Tutor(
                id_tutor=None,
                nome=form["nome"].strip(),
                cpf=cpf_limpo,
                telefone=form["telefone"],
                rg=form.get("rg") or None,
                cep=form.get("cep", "").replace("-", "").strip() or None,
                endereco=form.get("endereco") or None,
                numero=form.get("numero") or None,
                complemento=form.get("complemento") or None,
                bairro=form.get("bairro") or None,
                cidade=form.get("cidade") or None,
                estado=form.get("estado") or None,
                email=form.get("email") or None,
                horas_fora_casa=float(form["horas_fora_casa"])
                    if form.get("horas_fora_casa") else None,
                id_tipo_moradia=id_tipo_moradia,
                casa_telada=form.get("casa_telada") or None,
                acesso_quintal=form.get("acesso_quintal") or None,
                acesso_rua=form.get("acesso_rua") or None,
                autoriza_visita_ong=form.get("autoriza_visita_ong", "Não"),
                autoriza_foto_mural=form.get("autoriza_foto_mural", "Não"),
                observacoes=form.get("observacoes") or None,
            )
            id_tutor = tutor_repo.inserir(tutor)

        with AdocaoRepository() as adocao_repo:
            adocao = Adocao(
                id_adocao=None,
                id_animal=id_animal,
                id_tutor=id_tutor,
                id_status=1,  # Em análise
            )
            id_adocao = adocao_repo.inserir(adocao)

        return id_adocao

    def buscar_para_confirmacao(self, id_adocao: int) -> Optional[Adocao]:
        with AdocaoRepository() as repo:
            return repo.buscar_por_id(id_adocao)

    def buscar_para_pdf(self, id_adocao: int):
        """Retorna (adocao, animal, tutor) para geração do PDF."""
        with AdocaoRepository() as adocao_repo:
            adocao = adocao_repo.buscar_por_id(id_adocao)

        if not adocao:
            return None, None, None

        with AnimalRepository() as animal_repo:
            animal = animal_repo.buscar_por_id(adocao.id_animal)

        with TutorRepository() as tutor_repo:
            tutor = tutor_repo.buscar_por_id(adocao.id_tutor)

        return adocao, animal, tutor

    # ── Validações ───────────────────────────────────────────

    def _validar_animal_disponivel(self, id_animal: int) -> None:
        with AnimalRepository() as repo:
            animal = repo.buscar_por_id(id_animal)
        if not animal or animal.id_status != 1:
            raise ValueError("Animal não disponível para adoção.")

    def _validar_form_tutor(self, form: dict) -> None:
        if not form.get("nome", "").strip():
            raise ValueError("O nome do tutor é obrigatório.")
        cpf = form.get("cpf", "").replace(".", "").replace("-", "").strip()
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF inválido.")
        if not form.get("telefone", "").strip():
            raise ValueError("O telefone é obrigatório.")
        if form.get("autoriza_visita_ong") != "Sim":
            raise ValueError(
                "A autorização de visita da Cafofe é obrigatória "
                "para prosseguir com a adoção responsável."
            )
