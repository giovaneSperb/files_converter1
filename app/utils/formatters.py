def formatar_moeda(
    valor
):

    valor = float(
        valor
    )

    texto = f"{valor:,.2f}"

    texto = texto.replace(
        ",",
        "X"
    )

    texto = texto.replace(
        ".",
        ","
    )

    texto = texto.replace(
        "X",
        "."
    )

    return f"R$ {texto}"