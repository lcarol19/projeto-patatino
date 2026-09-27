from weasyprint import HTML
from flask import render_template
import io


def gerar_termo_pdf(adocao, animal, tutor):
    """Gera o PDF do termo de responsabilidade de adoção.
    Retorna bytes do PDF.
    """
    html_string = render_template(
        "termo_pdf.html",
        adocao=adocao,
        animal=animal,
        tutor=tutor,
    )
    pdf_bytes = HTML(string=html_string).write_pdf()
    return io.BytesIO(pdf_bytes)
