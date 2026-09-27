"""
AdocaoController — rotas do processo de adoção e geração de PDF.
"""
from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash, send_file, abort)
from services.adocao_service import AdocaoService
from services.pdf_service    import PDFService
from services.animal_service import AnimalService

adocao_bp   = Blueprint("adocao", __name__)
_adocao_svc = AdocaoService()
_animal_svc = AnimalService()
_pdf_svc    = PDFService()


@adocao_bp.route("/adotar/<int:id_animal>", methods=["GET", "POST"])
def adotar(id_animal: int):
    """Formulário de solicitação de adoção responsável."""
    animal = _animal_svc.buscar_por_id(id_animal)
    if not animal or animal.id_status != 1:
        flash("Animal não disponível para adoção.", "warning")
        return redirect(url_for("animal.home"))

    if request.method == "POST":
        try:
            id_adocao = _adocao_svc.solicitar(id_animal, request.form)
            flash(
                "Solicitação enviada! A Cafofe entrará em contato. 🐾",
                "success",
            )
            return redirect(url_for("adocao.confirmacao", id_adocao=id_adocao))
        except ValueError as e:
            flash(str(e), "warning")
        except Exception as e:
            flash(f"Erro inesperado: {e}", "danger")

    return render_template("adocao.html", animal=animal)


@adocao_bp.route("/adocao/confirmacao/<int:id_adocao>")
def confirmacao(id_adocao: int):
    """Página de confirmação após solicitação de adoção."""
    adocao = _adocao_svc.buscar_para_confirmacao(id_adocao)
    if not adocao:
        abort(404)
    return render_template("confirmacao_adocao.html", adocao=adocao)


@adocao_bp.route("/termo/<int:id_adocao>")
def termo_pdf(id_adocao: int):
    """Gera e retorna o PDF do termo de responsabilidade."""
    adocao, animal, tutor = _adocao_svc.buscar_para_pdf(id_adocao)
    if not adocao:
        abort(404)
    pdf = _pdf_svc.gerar_termo(adocao, animal, tutor)
    return send_file(
        pdf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"termo_adocao_{id_adocao}.pdf",
    )
