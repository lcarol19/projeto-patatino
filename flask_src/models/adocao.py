from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class FotoAdocao:
    """Foto registrada durante uma visita de acompanhamento."""
    id_foto_adocao: Optional[int]
    id_visita: int
    url_foto: str
    id_cloudinary: Optional[str]
    autorizada_divulgacao: bool = False
    data_cadastro: Optional[datetime] = None


@dataclass
class Visita:
    """Visita de acompanhamento pós-adoção realizada pela Cafofe."""
    id_visita: Optional[int]
    id_adocao: int
    data_visita: datetime
    id_resultado: Optional[int] = None
    resultado: Optional[str] = None         # campo enriquecido (JOIN)
    observacoes: Optional[str] = None
    data_cadastro: Optional[datetime] = None
    fotos: List[FotoAdocao] = field(default_factory=list)


@dataclass
class Adocao:
    """Representa uma solicitação ou processo de adoção."""
    id_adocao: Optional[int]
    id_animal: int
    id_tutor: int
    id_status: int = 1              # 1 = Em análise
    data_interesse: Optional[datetime] = None
    data_solicitacao: Optional[datetime] = None
    data_adocao: Optional[datetime] = None
    termo_gerado: bool = False
    observacoes: Optional[str] = None

    # campos enriquecidos (JOIN)
    status: Optional[str] = None
    nome_animal: Optional[str] = None
    nome_tutor: Optional[str] = None
    especie: Optional[str] = None
    visitas: List[Visita] = field(default_factory=list)

    @classmethod
    def from_dict(cls, dados: dict) -> "Adocao":
        return cls(
            id_adocao=dados.get("id_adocao"),
            id_animal=dados.get("id_animal", 0),
            id_tutor=dados.get("id_tutor", 0),
            id_status=dados.get("id_status", 1),
            data_interesse=dados.get("data_interesse"),
            data_solicitacao=dados.get("data_solicitacao"),
            data_adocao=dados.get("data_adocao"),
            termo_gerado=bool(dados.get("termo_gerado", False)),
            observacoes=dados.get("observacoes"),
            status=dados.get("status"),
            nome_animal=dados.get("nome_animal"),
            nome_tutor=dados.get("nome_tutor"),
            especie=dados.get("especie"),
        )
