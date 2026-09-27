"""
AnimalController — rotas relacionadas a animais.
Só chama services; zero SQL aqui.
"""
from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash, abort)
from services.animal_service import AnimalService

animal_bp = Blueprint("animal", __name__)
_service  = AnimalService()


@animal_bp.route("/")
def home():
    """Catálogo público de animais disponíveis para adoção."""
    especie = request.args.get("especie", "")
    porte   = request.args.get("porte", "")
    sexo    = request.args.get("sexo", "")
    busca   = request.args.get("q", "").strip()
    page    = request.args.get("page", 1, type=int)

    animais, total, total_paginas = _service.listar_catalogo(
        especie=especie, porte=porte, sexo=sexo,
        busca=busca, page=page,
    )

    return render_template(
        "home.html",
        animais=animais, total=total,
        page=page, total_paginas=total_paginas,
        especie=especie, porte=porte,
        sexo=sexo, busca=busca,
    )


@animal_bp.route("/animal/<int:id_animal>")
def detalhe(id_animal: int):
    """Detalhe do animal com carrossel de fotos."""
    animal = _service.buscar_por_id(id_animal)
    if not animal:
        abort(404)
    return render_template("animal.html", animal=animal)


@animal_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    """Formulário de acolhimento — cadastro de novo animal."""
    if request.method == "POST":
        try:
            arquivos  = request.files.getlist("fotos_animal")
            id_animal = _service.cadastrar(request.form, arquivos)
            flash("Animal cadastrado com sucesso! 🐾", "success")
            return redirect(url_for("animal.detalhe", id_animal=id_animal))
        except ValueError as e:
            flash(str(e), "warning")
        except Exception as e:
            flash(f"Erro inesperado: {e}", "danger")

    return render_template("cadastrar_animal.html")


@animal_bp.route("/editar/<int:id_animal>", methods=["GET", "POST"])
def editar(id_animal: int):
    """Edição de animal cadastrado."""
    if request.method == "POST":
        try:
            arquivos     = request.files.getlist("fotos_animal")
            fotos_remover = request.form.getlist("fotos_remover")
            _service.atualizar(id_animal, request.form, arquivos, fotos_remover)
            flash("Animal atualizado com sucesso! 🐾", "success")
            return redirect(url_for("animal.detalhe", id_animal=id_animal))
        except ValueError as e:
            flash(str(e), "warning")
        except Exception as e:
            flash(f"Erro inesperado: {e}", "danger")

    animal = _service.buscar_por_id(id_animal)
    if not animal:
        abort(404)
    return render_template("editar_animal.html", animal=animal)


@animal_bp.route("/excluir/<int:id_animal>", methods=["POST"])
def excluir(id_animal: int):
    """Remove animal e suas fotos do Cloudinary."""
    try:
        _service.excluir(id_animal)
        flash("Animal removido.", "info")
    except Exception as e:
        flash(f"Erro ao excluir: {e}", "danger")
    return redirect(url_for("animal.home"))
