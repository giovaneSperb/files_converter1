import os
import uuid

from flask import (
    Blueprint,
    request,
    jsonify,
    send_file,
    current_app
)

from app.services.retorno_service import (
    processar_preview,
    processar_retorno
)


pagamentos_bp = Blueprint(
    "pagamentos",
    __name__
)


def salvar_arquivo_upload():

    if "arquivo" not in request.files:

        raise ValueError(
            "Nenhum arquivo foi enviado."
        )

    arquivo = request.files[
        "arquivo"
    ]

    if arquivo.filename == "":

        raise ValueError(
            "Nome do arquivo não informado."
        )

    extensao = os.path.splitext(
        arquivo.filename
    )[1].lower()

    extensoes_permitidas = [
        ".ret",
        ".txt"
    ]

    if extensao not in (
        extensoes_permitidas
    ):

        raise ValueError(
            "O arquivo deve possuir "
            "extensão .RET ou .TXT."
        )

    nome_arquivo = (
        f"{uuid.uuid4().hex}"
        f"{extensao}"
    )

    caminho_arquivo = os.path.join(

        current_app.config[
            "UPLOAD_FOLDER"
        ],

        nome_arquivo

    )

    arquivo.save(
        caminho_arquivo
    )

    return caminho_arquivo


@pagamentos_bp.route(
    "/preview",
    methods=["POST"]
)
def preview_arquivo():

    try:

        caminho_arquivo = (
            salvar_arquivo_upload()
        )

        resultado = processar_preview(

            caminho_arquivo

        )

        return jsonify(
            resultado
        ), 200

    except ValueError as erro:

        return jsonify({

            "erro": str(
                erro
            )

        }), 400

    except Exception as erro:

        return jsonify({

            "erro": (
                "Erro ao processar "
                "arquivo."
            ),

            "detalhes": str(
                erro
            )

        }), 500


@pagamentos_bp.route(
    "/importar",
    methods=["POST"]
)
def importar_arquivo():

    try:

        caminho_arquivo = (
            salvar_arquivo_upload()
        )

        caminho_pdf = (
            processar_retorno(

                caminho_arquivo

            )
        )

        return send_file(

            caminho_pdf,

            mimetype=(
                "application/pdf"
            ),

            as_attachment=True,

            download_name=(
                "relatorio_pagamentos.pdf"
            )

        )

    except ValueError as erro:

        return jsonify({

            "erro": str(
                erro
            )

        }), 400

    except Exception as erro:

        return jsonify({

            "erro": (
                "Erro ao processar "
                "arquivo."
            ),

            "detalhes": str(
                erro
            )

        }), 500