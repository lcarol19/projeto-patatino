"""
CEPService — consulta de endereço via API pública ViaCEP.
Requisito do PI: uso de API externa.
"""
import requests
from typing import Optional


class CEPService:
    """Consulta a API ViaCEP e retorna dados do endereço."""

    BASE_URL = "https://viacep.com.br/ws/{cep}/json/"
    TIMEOUT  = 5  # segundos

    def buscar(self, cep: str) -> Optional[dict]:
        """
        Recebe um CEP (com ou sem hífen), consulta ViaCEP
        e retorna um dicionário com logradouro, bairro, cidade, estado.
        Retorna None se o CEP for inválido ou o serviço falhar.
        """
        cep_limpo = self._limpar(cep)
        if not self._validar(cep_limpo):
            return None

        try:
            resp = requests.get(
                self.BASE_URL.format(cep=cep_limpo),
                timeout=self.TIMEOUT,
            )
            dados = resp.json()
            if "erro" in dados:
                return None
            return {
                "cep":       dados.get("cep", ""),
                "endereco":  dados.get("logradouro", ""),
                "bairro":    dados.get("bairro", ""),
                "cidade":    dados.get("localidade", ""),
                "estado":    dados.get("uf", ""),
            }
        except (requests.RequestException, ValueError):
            return None

    @staticmethod
    def _limpar(cep: str) -> str:
        return cep.replace("-", "").replace(".", "").strip()

    @staticmethod
    def _validar(cep: str) -> bool:
        return len(cep) == 8 and cep.isdigit()
