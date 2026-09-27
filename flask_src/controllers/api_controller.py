"""
APIController — endpoints JSON da aplicação.
Requisito PI: uso de API (ViaCEP).
"""
from flask import Blueprint, jsonify
from services.cep_service import CEPService

api_bp   = Blueprint("api", __name__)
_cep_svc = CEPService()


@api_bp.route("/cep/<cep>")
def buscar_cep(cep: str):
    """
    Proxy para ViaCEP — usado pelo JavaScript do formulário de adoção
    para preencher o endereço automaticamente ao digitar o CEP.

    GET /api/cep/01310100
    Retorna: { cep, endereco, bairro, cidade, estado }
    """
    dados = _cep_svc.buscar(cep)
    if not dados:
        return jsonify({"erro": "CEP não encontrado ou inválido."}), 404
    return jsonify(dados)
