import os

from flask import current_app

from app.parsers.retorno_parser import (
    ler_arquivo_retorno
)

from app.services.pdf_service import (
    gerar_pdf_pagamentos
)


def carregar_pagamentos(
    caminho_arquivo
):

    pagamentos = ler_arquivo_retorno(

        caminho_arquivo

    )

    if not pagamentos:

        raise ValueError(

            "Nenhum pagamento encontrado "
            "no arquivo CNAB 240."

        )

    return pagamentos


def processar_preview(
    caminho_arquivo
):

    pagamentos = carregar_pagamentos(

        caminho_arquivo

    )

    valor_total = sum(

        (

            pagamento.get(
                "valor",
                0
            )

            or 0

        )

        for pagamento
        in pagamentos

    )

    pagamentos_ordenados = sorted(

        pagamentos,

        key=lambda pagamento:

            pagamento.get(
                "valor",
                0
            ) or 0,

        reverse=True

    )

    return {

        "arquivo": os.path.basename(

            caminho_arquivo

        ),

        "total_pagamentos": len(

            pagamentos

        ),

        "valor_total": round(

            valor_total,

            2

        ),

        "pagamentos": (

            pagamentos_ordenados

        )

    }


def processar_retorno(
    caminho_arquivo
):

    pagamentos = carregar_pagamentos(

        caminho_arquivo

    )

    pagamentos.sort(

        key=lambda pagamento:

            pagamento.get(
                "valor",
                0
            ) or 0,

        reverse=True

    )

    nome_pdf = (

        "relatorio_pagamentos.pdf"

    )

    caminho_pdf = os.path.join(

        current_app.config[
            "OUTPUT_FOLDER"
        ],

        nome_pdf

    )

    gerar_pdf_pagamentos(

        pagamentos,

        caminho_pdf

    )

    return caminho_pdf