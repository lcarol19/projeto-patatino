"""
PDFService — geração do termo de responsabilidade em PDF.
Usa ReportLab (funciona no Windows sem dependências externas).
"""
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


class PDFService:
    """Gera o termo de responsabilidade de adoção em PDF."""

    # Cores Cafofe
    LARANJA = colors.HexColor('#f28b00')
    ESCURO  = colors.HexColor('#1a1a2e')
    CINZA   = colors.HexColor('#f8f9fa')

    def gerar_termo(self, adocao, animal, tutor) -> io.BytesIO:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2.5*cm,
            leftMargin=2.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
        )

        styles   = getSampleStyleSheet()
        elements = []

        # ── Estilos ──────────────────────────────────────────
        titulo_style = ParagraphStyle(
            'titulo', parent=styles['Title'],
            textColor=self.LARANJA,
            fontSize=16, spaceAfter=4,
        )
        subtitulo_style = ParagraphStyle(
            'subtitulo', parent=styles['Heading2'],
            textColor=self.ESCURO,
            fontSize=13, spaceAfter=2,
        )
        secao_style = ParagraphStyle(
            'secao', parent=styles['Heading3'],
            textColor=self.ESCURO,
            fontSize=11, spaceBefore=12, spaceAfter=6,
            borderPad=4,
        )
        normal_style = ParagraphStyle(
            'normal_cafofe', parent=styles['Normal'],
            fontSize=10, spaceAfter=4,
            alignment=TA_JUSTIFY,
        )
        center_style = ParagraphStyle(
            'center_cafofe', parent=styles['Normal'],
            fontSize=9, alignment=TA_CENTER,
            textColor=colors.grey,
        )
        label_style = ParagraphStyle(
            'label', parent=styles['Normal'],
            fontSize=10, textColor=colors.HexColor('#495057'),
            fontName='Helvetica-Bold',
        )

        # ── Cabeçalho ────────────────────────────────────────
        elements.append(Paragraph('CAFOFE — Casa dos Focinhos Felizes!', titulo_style))
        elements.append(Paragraph('Termo de Responsabilidade de Adoção', subtitulo_style))
        elements.append(Paragraph(
            'contato@cafofe.org  |  (11) 9 8692-1947  |  www.cafofe.org',
            center_style,
        ))
        elements.append(HRFlowable(width='100%', thickness=2,
                                    color=self.LARANJA, spaceAfter=8))

        # Protocolo
        data_str = (adocao.data_interesse.strftime('%d/%m/%Y')
                    if adocao.data_interesse else '—')
        proto_data = [
            [Paragraph('<b>Protocolo:</b>', normal_style),
             Paragraph(f'#{adocao.id_adocao:05d}', normal_style),
             Paragraph('<b>Data:</b>', normal_style),
             Paragraph(data_str, normal_style)],
        ]
        proto_table = Table(proto_data, colWidths=[3*cm, 5*cm, 2.5*cm, 5*cm])
        proto_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), self.CINZA),
            ('BOX',        (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('PADDING',    (0,0), (-1,-1), 6),
        ]))
        elements.append(proto_table)
        elements.append(Spacer(1, 10))

        # ── Dados do animal ───────────────────────────────────
        elements.append(Paragraph('Dados do Animal', secao_style))
        elements.append(HRFlowable(width='40%', thickness=2,
                                    color=self.LARANJA, spaceAfter=6))

        animal_rows = [
            ['Nome',            animal.nome],
            ['Espécie',         animal.especie or '—'],
            ['Porte',           animal.porte   or '—'],
            ['Sexo',            animal.sexo    or '—'],
            ['Idade aproximada', animal.idade_legivel],
            ['Código do chip',  animal.codigo_chip or '—'],
        ]
        elements.append(self._tabela_dados(animal_rows, normal_style))
        elements.append(Spacer(1, 8))

        # ── Dados do tutor ────────────────────────────────────
        elements.append(Paragraph('Dados do Adotante', secao_style))
        elements.append(HRFlowable(width='40%', thickness=2,
                                    color=self.LARANJA, spaceAfter=6))

        tutor_rows = [
            ['Nome completo',   tutor.nome],
            ['CPF',             tutor.cpf_formatado],
            ['RG',              tutor.rg       or '—'],
            ['Telefone',        tutor.telefone],
            ['E-mail',          tutor.email    or '—'],
            ['Endereço',        tutor.endereco_completo or '—'],
            ['Tipo de moradia', tutor.tipo_moradia or '—'],
            ['Horas fora/dia',  str(tutor.horas_fora_casa) + 'h' if tutor.horas_fora_casa else '—'],
            ['Autoriza visitas', tutor.autoriza_visita_ong],
        ]
        elements.append(self._tabela_dados(tutor_rows, normal_style))
        elements.append(Spacer(1, 8))

        # ── Cláusulas ─────────────────────────────────────────
        elements.append(Paragraph('Cláusulas e Condições', secao_style))
        elements.append(HRFlowable(width='40%', thickness=2,
                                    color=self.LARANJA, spaceAfter=6))

        clausulas = [
            'O adotante declara ter <b>mais de 21 anos</b> e estar ciente de todas as responsabilidades inerentes à adoção de um animal.',
            'O adotante compromete-se a proporcionar ao animal <b>conforto, saúde e bem-estar</b>, incluindo alimentação adequada, cuidados veterinários e atenção afetiva.',
            'A residência do adotante deve ser <b>adaptada e segura</b> para o animal, evitando fugas ou acidentes. Para gatos, a tela de proteção nas janelas é obrigatória.',
            'O adotante compromete-se a <b>não repassar ou abandonar</b> o animal sem antes entrar em contato com a Cafofe.',
            'O adotante <b>autoriza visitas periódicas</b> de membros da Cafofe para verificação do bem-estar do animal.',
            'Em caso de descumprimento das cláusulas, a Cafofe reserva-se o direito de <b>resgatar o animal</b>.',
        ]
        for i, texto in enumerate(clausulas, 1):
            elements.append(Paragraph(f'{i}. {texto}', normal_style))

        elements.append(Spacer(1, 24))

        # ── Assinaturas ───────────────────────────────────────
        assin_data = [
            ['_'*40, '', '_'*40],
            [tutor.nome, '', 'CAFOFE — Casa dos Focinhos Felizes'],
            [f'CPF: {tutor.cpf_formatado}', '', 'CNPJ: 67.784.880/0001-05'],
            ['Adotante', '', 'Representante'],
        ]
        assin_table = Table(assin_data, colWidths=[7*cm, 2*cm, 7*cm])
        assin_table.setStyle(TableStyle([
            ('ALIGN',    (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('TEXTCOLOR',(0,1), (-1,-1), colors.HexColor('#495057')),
        ]))
        elements.append(assin_table)
        elements.append(Spacer(1, 16))

        # ── Rodapé ────────────────────────────────────────────
        elements.append(HRFlowable(width='100%', thickness=0.5,
                                    color=colors.lightgrey, spaceAfter=4))
        data_hora = (adocao.data_interesse.strftime('%d/%m/%Y às %H:%M')
                     if adocao.data_interesse else '—')
        elements.append(Paragraph(
            f'Documento gerado pela plataforma PATATINO em {data_hora}. '
            f'Protocolo #{adocao.id_adocao:05d}',
            center_style,
        ))

        doc.build(elements)
        buffer.seek(0)
        return buffer

    def _tabela_dados(self, rows: list, style) -> Table:
        """Cria uma tabela de dois campos: label | valor."""
        data = []
        for label, valor in rows:
            data.append([
                Paragraph(f'<b>{label}</b>', style),
                Paragraph(str(valor), style),
            ])
        table = Table(data, colWidths=[5*cm, 11*cm])
        table.setStyle(TableStyle([
            ('VALIGN',     (0,0), (-1,-1), 'TOP'),
            ('PADDING',    (0,0), (-1,-1), 5),
            ('ROWBACKGROUNDS', (0,0), (-1,-1),
             [colors.white, self.CINZA]),
            ('GRID',       (0,0), (-1,-1), 0.3, colors.lightgrey),
        ]))
        return table
