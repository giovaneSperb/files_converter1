from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image as ReportLabImage
)

from app.utils.formatters import formatar_moeda


CAMINHO_LOGO_CAIXA = (
    Path(__file__).resolve().parent.parent
    / "assets"
    / "caixa_logo.png"
)


def criar_estilos():

    estilos_base = getSampleStyleSheet()

    estilos = {}

    estilos["titulo_caixa"] = ParagraphStyle(
        "TituloCaixa",
        parent=estilos_base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        alignment=TA_LEFT
    )

    estilos["texto"] = ParagraphStyle(
        "Texto",
        parent=estilos_base["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        alignment=TA_LEFT
    )

    estilos["texto_bold"] = ParagraphStyle(
        "TextoBold",
        parent=estilos_base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        alignment=TA_LEFT
    )

    estilos["logo"] = ParagraphStyle(
        "Logo",
        parent=estilos_base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=26,
        alignment=TA_LEFT
    )

    estilos["rodape"] = ParagraphStyle(
        "Rodape",
        parent=estilos_base["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=10,
        alignment=TA_LEFT
    )

    return estilos


def criar_linha(
    label,
    valor,
    estilos
):

    return [
        Paragraph(
            str(label),
            estilos["texto"]
        ),

        Paragraph(
            str(valor or ""),
            estilos["texto"]
        )
    ]


def criar_caixa(
    dados,
    estilos
):

    tabela = Table(
        dados,
        colWidths=[
            80 * mm,
            90 * mm
        ]
    )

    tabela.setStyle(
        TableStyle(
            [

                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.black
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )

            ]
        )
    )

    return tabela


def obter_tipo_transferencia(
    pagamento
):

    if pagamento.get("banco_favorecido", "").strip() == "104":

        return "TEV"

    return "TED"


def criar_comprovante(
    pagamento,
    estilos
):

    elementos = []

    tipo_transferencia = obter_tipo_transferencia(
        pagamento
    )

    # ==================================================
    # CABEÇALHO
    # ==================================================

    logo_caixa = ReportLabImage(
        str(CAMINHO_LOGO_CAIXA),
        width=42 * mm,
        height=9.6 * mm
    )

    logo_caixa.hAlign = "LEFT"

    elementos.append(
        logo_caixa
    )

    elementos.append(
        Spacer(
            1,
            2
        )
    )

    elementos.append(
        Paragraph(
            (
                "Comprovante de Transferência "
                "entre contas da CAIXA - "
                f"{tipo_transferencia}"
            ),
            estilos["titulo_caixa"]
        )
    )

    elementos.append(
        Spacer(
            1,
            8
        )
    )

    elementos.append(
        Paragraph(
            (
                "Transação realizada via "
                "convênio de pagamentos"
            ),
            estilos["texto"]
        )
    )

    elementos.append(
        Spacer(
            1,
            15
        )
    )

    # ==================================================
    # DADOS DO EMITENTE
    # ==================================================

    dados_emitente = [

        criar_linha(
            "Nome do remetente:",
            "PORTAL ADMINISTRACAO DE IMOVEI",
            estilos
        ),

        criar_linha(
            "CNPJ/CPF:",
            "94.698.313/0001-09",
            estilos
        ),

        criar_linha(
            "Tipo de pessoa:",
            "Jurídica",
            estilos
        ),

        criar_linha(
            "Conta de origem:",
            "6352.003.00028883-2",
            estilos
        )

    ]

    if tipo_transferencia == "TED":

        dados_emitente.append(
            criar_linha(
                "Tipo de conta:",
                "03 - Conta pessoa juridica",
                estilos
            )
        )

    emitente = criar_caixa(
        dados_emitente,
        estilos
    )

    elementos.append(
        emitente
    )

    elementos.append(
        Spacer(
            1,
            12
        )
    )

    # ==================================================
    # DADOS DO CONVÊNIO
    # ==================================================

    if tipo_transferencia == "TED":

        dados_convenio = pagamento.copy()

        descricoes_tipo_compromisso = {
            "0001": "Pagamento a Fornecedor"
        }

        descricoes_compromisso = {
            "0003": "Pagamento a Fornecedor"
        }

        tipo_compromisso = dados_convenio.get(
            "tipo_compromisso",
            ""
        )

        compromisso = dados_convenio.get(
            "compromisso",
            ""
        )

        if tipo_compromisso in descricoes_tipo_compromisso:

            dados_convenio["tipo_compromisso"] = (
                f"{tipo_compromisso} - "
                f"{descricoes_tipo_compromisso[tipo_compromisso]}"
            )

        if compromisso in descricoes_compromisso:

            dados_convenio["compromisso"] = (
                f"{compromisso} - "
                f"{descricoes_compromisso[compromisso]}"
            )

    else:

        dados_convenio = pagamento

    numero_convenio = dados_convenio.get(
        "convenio",
        ""
    )

    nome_convenio = pagamento.get(
        "nome_emitente",
        ""
    )

    if numero_convenio and nome_convenio:

        valor_convenio = (
            f"{numero_convenio} - {nome_convenio}"
        )

    else:

        valor_convenio = numero_convenio

    convenio = criar_caixa(
        [

            criar_linha(
                "Convênio:",
                valor_convenio,
                estilos
            ),

            criar_linha(
                "Tipo de compromisso:",
                dados_convenio.get(
                    "tipo_compromisso",
                    ""
                ),
                estilos
            ),

            criar_linha(
                "Compromisso:",
                dados_convenio.get(
                    "compromisso",
                    ""
                ),
                estilos
            ),

            criar_linha(
                "NSA:",
                dados_convenio.get(
                    "nsa",
                    ""
                ),
                estilos
            )

        ],
        estilos
    )

    elementos.append(
        convenio
    )

    elementos.append(
        Spacer(
            1,
            12
        )
    )

    # ==================================================
    # DADOS DO DESTINATÁRIO
    # ==================================================

    valor = pagamento.get(
        "valor",
        0
    ) or 0

    if tipo_transferencia == "TED":

        codigo_banco = pagamento.get(
            "banco_favorecido",
            ""
        )

        nome_banco = pagamento.get(
            "nome_banco_favorecido",
            ""
        )

        banco_destino = (
            f"{codigo_banco} - {nome_banco}"
            if nome_banco
            else codigo_banco
        )

        agencia = pagamento.get(
            "agencia_favorecido",
            ""
        )

        conta = pagamento.get(
            "conta_favorecido",
            ""
        )

        digito_conta = pagamento.get(
            "digito_conta_favorecido",
            ""
        )

        agencia_conta = f"{agencia}/{conta}"

        if digito_conta:

            agencia_conta = f"{agencia_conta}-{digito_conta}"

        tipo_conta = pagamento.get(
            "tipo_conta_favorecido",
            ""
        )

        descricao_tipo_conta = {
            "0": "Sem conta"
        }.get(tipo_conta, "")

        tipo_conta_destino = (
            f"{tipo_conta} - {descricao_tipo_conta}"
            if descricao_tipo_conta
            else tipo_conta
        )

        dados_destinatario = [

            criar_linha(
                "Banco destino:",
                banco_destino,
                estilos
            ),

            criar_linha(
                "Agência/Conta destino:",
                agencia_conta,
                estilos
            ),

            criar_linha(
                "Tipo de conta:",
                tipo_conta_destino,
                estilos
            ),

            criar_linha(
                "Tipo de pessoa:",
                pagamento.get(
                    "tipo_pessoa_favorecido",
                    ""
                ),
                estilos
            ),

            criar_linha(
                "Nome do destinatário:",
                pagamento.get(
                    "nome",
                    ""
                ),
                estilos
            ),

            criar_linha(
                "CPF/CNPJ do destinatário:",
                pagamento.get(
                    "cpf_cnpj",
                    ""
                ),
                estilos
            )

        ]

    else:

        dados_destinatario = [

            criar_linha(
                "Conta destino:",
                pagamento.get(
                    "conta_favorecido",
                    ""
                ),
                estilos
            ),

            criar_linha(
                "Nome do destinatário:",
                pagamento.get(
                    "nome",
                    ""
                ),
                estilos
            )

        ]

    dados_destinatario.extend(
        [

            criar_linha(
                "Valor:",
                formatar_moeda(
                    valor
                ),
                estilos
            ),

            criar_linha(
                "Data da operação:",
                pagamento.get(
                    "data_pagamento",
                    ""
                ),
                estilos
            )

        ]
    )

    destinatario = criar_caixa(
        dados_destinatario,
        estilos
    )

    elementos.append(
        destinatario
    )

    # ==================================================
    # ESPAÇO ANTES DA AUTENTICAÇÃO
    # ==================================================

    elementos.append(
        Spacer(
            1,
            25
        )
    )

    # ==================================================
    # AUTENTICAÇÃO BANCÁRIA
    # ==================================================

    autenticacao = criar_caixa(
        [

            criar_linha(
                "Autenticação Bancária:",
                pagamento.get(
                    "autenticacao",
                    ""
                ),
                estilos
            )

        ],
        estilos
    )

    elementos.append(
        autenticacao
    )

    elementos.append(
        Spacer(
            1,
            20
        )
    )

    # ==================================================
    # MENSAGEM
    # ==================================================

    elementos.append(
        Paragraph(
            (
                "Operação realizada com sucesso "
                "conforme as informações enviadas "
                "pelo cliente via arquivo."
            ),
            estilos["texto_bold"]
        )
    )

    elementos.append(
        Spacer(
            1,
            20
        )
    )

    # ==================================================
    # RODAPÉ
    # ==================================================

    elementos.append(
        Paragraph(
            "SAC CAIXA: 0800 726 0101",
            estilos["rodape"]
        )
    )

    elementos.append(
        Spacer(
            1,
            5
        )
    )

    elementos.append(
        Paragraph(
            (
                "Pessoas com deficiência auditiva: "
                "0800 726 2492"
            ),
            estilos["rodape"]
        )
    )

    elementos.append(
        Spacer(
            1,
            5
        )
    )

    elementos.append(
        Paragraph(
            "Ouvidoria: 0800 725 7474",
            estilos["rodape"]
        )
    )

    elementos.append(
        Spacer(
            1,
            5
        )
    )

    elementos.append(
        Paragraph(
            "Help Desk CAIXA: 0800 726 0104",
            estilos["rodape"]
        )
    )

    return elementos


def gerar_pdf_pagamentos(
    pagamentos,
    caminho_pdf
):

    documento = SimpleDocTemplate(

        caminho_pdf,

        pagesize=A4,

        rightMargin=20 * mm,

        leftMargin=20 * mm,

        topMargin=12 * mm,

        bottomMargin=15 * mm

    )

    estilos = criar_estilos()

    elementos = []

    # ==================================================
    # ORDENAÇÃO POR VALOR
    # MAIOR PARA O MENOR
    # ==================================================

    pagamentos_ordenados = sorted(

        pagamentos,

        key=lambda pagamento:

            pagamento.get(
                "valor",
                0
            ) or 0,

        reverse=True

    )

    # ==================================================
    # GERA UM COMPROVANTE POR PÁGINA
    # ==================================================

    for indice, pagamento in enumerate(
        pagamentos_ordenados
    ):

        comprovante = criar_comprovante(

            pagamento,

            estilos

        )

        elementos.extend(
            comprovante
        )

        if (
            indice
            < len(
                pagamentos_ordenados
            ) - 1
        ):

            elementos.append(
                PageBreak()
            )

    documento.build(
        elementos
    )
