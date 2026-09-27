"""
app.py — ponto de entrada da aplicação Flask.
Controllers registrados como Blueprints.
Nenhuma regra de negócio aqui.
"""
import os
from flask import Flask
from dotenv import load_dotenv
from config import Config

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# ── Filtro Jinja2: formata preço BR ──────────────────────────
app.jinja_env.filters["preco_br"] = (
    lambda v: f"{float(v):_.2f}".replace(".", ",").replace("_", ".")
    if v else ""
)

# ── Blueprints (controllers) ─────────────────────────────────
from controllers.animal_controller import animal_bp
from controllers.adocao_controller import adocao_bp
from controllers.api_controller    import api_bp

app.register_blueprint(animal_bp)
app.register_blueprint(adocao_bp)
app.register_blueprint(api_bp, url_prefix="/api")

# ── Páginas de erro ──────────────────────────────────────────
from flask import render_template

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def erro_interno(e):
    return render_template("500.html"), 500

# ── Execução local ───────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
