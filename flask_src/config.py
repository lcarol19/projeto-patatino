import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("APP_SECRET_KEY", "patatino-dev-secret")
    MAX_FOTOS_ANIMAL = 3
    ESPECIES = ["Cachorro", "Gato", "Outro"]
    PORTES = ["Pequeno", "Médio", "Grande"]
    SEXOS = ["Macho", "Fêmea", "Não informado"]
    STATUS_ANIMAL = ["Para adoção", "Adotado", "Em tratamento", "Óbito"]
    STATUS_ADOCAO = ["Em análise", "Aprovada", "Recusada", "Cancelada", "Concluída"]
    TIPOS_MORADIA = ["Casa", "Apartamento", "Sítio", "Comércio", "Outros"]
    RESPOSTAS_SIM_NAO = ["Sim", "Não"]
    RESPOSTAS_MORADIA = ["Sim", "Não", "Não se aplica"]
