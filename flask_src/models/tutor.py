from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Tutor:
    """Representa um tutor (candidato à adoção)."""
    id_tutor: Optional[int]
    nome: str
    cpf: str                        # apenas dígitos
    telefone: str
    rg: Optional[str] = None
    cep: Optional[str] = None
    endereco: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    email: Optional[str] = None
    horas_fora_casa: Optional[float] = None
    id_tipo_moradia: Optional[int] = None
    tipo_moradia: Optional[str] = None      # campo enriquecido (JOIN)
    casa_telada: Optional[str] = None
    acesso_quintal: Optional[str] = None
    acesso_rua: Optional[str] = None
    autoriza_visita_ong: str = "Sim"
    autoriza_foto_mural: str = "Sim"
    observacoes: Optional[str] = None
    data_cadastro: Optional[datetime] = None

    @property
    def cpf_formatado(self) -> str:
        """Retorna CPF no formato 000.000.000-00."""
        c = self.cpf.zfill(11)
        return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"

    @property
    def endereco_completo(self) -> str:
        partes = [self.endereco]
        if self.numero:
            partes.append(f"nº {self.numero}")
        if self.complemento:
            partes.append(self.complemento)
        if self.bairro:
            partes.append(self.bairro)
        if self.cidade and self.estado:
            partes.append(f"{self.cidade}/{self.estado}")
        return ", ".join(p for p in partes if p)

    @classmethod
    def from_dict(cls, dados: dict) -> "Tutor":
        return cls(
            id_tutor=dados.get("id_tutor"),
            nome=dados.get("nome", ""),
            cpf=dados.get("cpf", ""),
            telefone=dados.get("telefone", ""),
            rg=dados.get("rg"),
            cep=dados.get("cep"),
            endereco=dados.get("endereco"),
            numero=dados.get("numero"),
            complemento=dados.get("complemento"),
            bairro=dados.get("bairro"),
            cidade=dados.get("cidade"),
            estado=dados.get("estado"),
            email=dados.get("email"),
            horas_fora_casa=dados.get("horas_fora_casa"),
            id_tipo_moradia=dados.get("id_tipo_moradia"),
            tipo_moradia=dados.get("tipo_moradia"),
            casa_telada=dados.get("casa_telada"),
            acesso_quintal=dados.get("acesso_quintal"),
            acesso_rua=dados.get("acesso_rua"),
            autoriza_visita_ong=dados.get("autoriza_visita_ong", "Sim"),
            autoriza_foto_mural=dados.get("autoriza_foto_mural", "Sim"),
            observacoes=dados.get("observacoes"),
            data_cadastro=dados.get("data_cadastro"),
        )
