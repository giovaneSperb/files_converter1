def formatar_cpf(
    cpf
):

    digitos = "".join(c for c in cpf if c.isdigit())

    # campo CNAB pode vir zero-padded com dígitos a mais
    if len(digitos) > 11:

        digitos = digitos[-11:]

    if len(digitos) == 11:

        return (
            f"{digitos[0:3]}."
            f"{digitos[3:6]}."
            f"{digitos[6:9]}-"
            f"{digitos[9:11]}"
        )

    return cpf


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