"""
Modelos de dados — entidades do domínio.
Representam as tabelas do banco sem depender do banco.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class FotoAnimal:
    """Representa uma foto vinculada a um animal."""
    id_foto: Optional[int]
    id_animal: int
    url_foto: str
    id_cloudinary: Optional[str]
    ordem: int
    data_cadastro: Optional[datetime] = None


@dataclass
class Animal:
    """Representa um animal cadastrado na plataforma."""
    id_animal: Optional[int]
    nome: str
    id_especie: int
    id_porte: int
    id_status: int = 1          # 1 = Para adoção (padrão)
    sexo: str = "Não informado"
    idade_aproximada: Optional[int] = None   # em meses
    codigo_chip: Optional[str] = None
    temperamento: Optional[str] = None
    descricao: Optional[str] = None
    observacoes: Optional[str] = None
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None

    # campos enriquecidos (JOIN) — não vêm do INSERT
    especie: Optional[str] = None
    porte: Optional[str] = None
    status: Optional[str] = None
    fotos: List[FotoAnimal] = field(default_factory=list)

    @property
    def foto_principal(self) -> str:
        """Retorna a URL da primeira foto ou string vazia."""
        return self.fotos[0].url_foto if self.fotos else ""

    @property
    def idade_legivel(self) -> str:
        """Converte meses para texto legível."""
        if not self.idade_aproximada:
            return "Não informada"
        anos = self.idade_aproximada // 12
        meses = self.idade_aproximada % 12
        if anos == 0:
            return f"{meses} {'mês' if meses == 1 else 'meses'}"
        if meses == 0:
            return f"{anos} {'ano' if anos == 1 else 'anos'}"
        return f"{anos} {'ano' if anos == 1 else 'anos'} e {meses} {'mês' if meses == 1 else 'meses'}"

    @classmethod
    def from_dict(cls, dados: dict) -> "Animal":
        """Cria um Animal a partir de um dicionário (cursor.fetchone)."""
        return cls(
            id_animal=dados.get("id_animal"),
            nome=dados.get("nome", ""),
            id_especie=dados.get("id_especie", 0),
            id_porte=dados.get("id_porte", 0),
            id_status=dados.get("id_status", 1),
            sexo=dados.get("sexo", "Não informado"),
            idade_aproximada=dados.get("idade_aproximada"),
            codigo_chip=dados.get("codigo_chip"),
            temperamento=dados.get("temperamento"),
            descricao=dados.get("descricao"),
            observacoes=dados.get("observacoes"),
            data_cadastro=dados.get("data_cadastro"),
            data_atualizacao=dados.get("data_atualizacao"),
            especie=dados.get("especie"),
            porte=dados.get("porte"),
            status=dados.get("status"),
        )
