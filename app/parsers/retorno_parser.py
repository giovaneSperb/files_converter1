from decimal import Decimal, InvalidOperation


class CNAB240Parser:

    def __init__(self, caminho_arquivo):

        self.caminho_arquivo = caminho_arquivo

        self.codigo_banco = ""

        self.nome_emitente = ""

        self.documento_emitente = ""

        self.conta_origem = ""

        self.convenio = ""

        self.tipo_compromisso = ""

        self.compromisso = ""

        self.nsa = ""

        self.pagamentos = []

        self.pagamento_atual = None

    def parse(self):

        with open(
            self.caminho_arquivo,
            "r",
            encoding="latin-1"
        ) as arquivo:

            for linha in arquivo:

                linha = linha.rstrip(
                    "\r\n"
                )

                if not linha:

                    continue

                if len(linha) < 240:

                    continue

                tipo_registro = linha[7:8]

                if tipo_registro == "0":

                    self._processar_header_arquivo(
                        linha
                    )

                elif tipo_registro == "1":

                    self._processar_header_lote(
                        linha
                    )

                elif tipo_registro == "3":

                    self._processar_segmento(
                        linha
                    )

                elif tipo_registro == "5":

                    self._finalizar_pagamento()

                elif tipo_registro == "9":

                    self._finalizar_pagamento()

        self._finalizar_pagamento()

        return self.pagamentos

    def _processar_header_arquivo(
        self,
        linha
    ):

        self.codigo_banco = (
            linha[0:3].strip()
        )

        self.nome_emitente = (
            linha[72:102].strip()
        )

        tipo_inscricao_emitente = (
            linha[17:18].strip()
        )

        documento_emitente = (
            linha[18:32].strip()
        )

        self.documento_emitente = (
            self._formatar_cpf_cnpj(
                tipo_inscricao_emitente,
                documento_emitente
            )
        )

        self.nsa = (
            linha[157:163].strip()
        )

    def _processar_header_lote(
        self,
        linha
    ):

        self.convenio = (
            linha[32:38].strip()
        )

        self.tipo_compromisso = (
            linha[38:40].strip().zfill(4)
        )

        self.compromisso = (
            linha[40:44].strip().zfill(4)
        )

        self.conta_origem = (
            linha[58:70].strip()
        )

    def _processar_segmento(
        self,
        linha
    ):

        codigo_segmento = (
            linha[13:14]
        )

        if codigo_segmento == "A":

            self._finalizar_pagamento()

            self._processar_segmento_a(
                linha
            )

        elif codigo_segmento == "B":

            self._processar_segmento_b(
                linha
            )

        elif codigo_segmento == "Z":

            self._processar_segmento_z(
                linha
            )

    def _processar_segmento_a(
        self,
        linha
    ):

        valor = self._converter_valor(
            linha[119:134]
        )

        data_pagamento = (
            linha[93:101].strip()
        )

        banco_favorecido = (
            linha[20:23].strip()
        )

        agencia_favorecido = (
            linha[23:28].strip()
        )

        conta_favorecido = (
            linha[29:41].strip()
        )

        digito_conta_favorecido = (
            linha[41:42].strip()
        )

        tipo_conta_favorecido = (
            linha[17:18].strip()
        )

        nome_destinatario = (
            linha[43:73].strip()
        )

        self.pagamento_atual = {

            "codigo_banco": (
                self.codigo_banco
            ),

            "nome_emitente": (
                self.nome_emitente
            ),

            "documento_emitente": (
                self.documento_emitente
            ),

            "conta_origem": (
                self.conta_origem
            ),

            "convenio": (
                self.convenio
            ),

            "tipo_compromisso": (
                self.tipo_compromisso
            ),

            "compromisso": (
                self.compromisso
            ),

            "nsa": (
                self.nsa
            ),

            "banco_favorecido": (
                banco_favorecido
            ),

            "nome_banco_favorecido": (
                self._obter_nome_banco(
                    banco_favorecido
                )
            ),

            "agencia_favorecido": (
                agencia_favorecido
            ),

            "conta_favorecido": (
                conta_favorecido
            ),

            "digito_conta_favorecido": (
                digito_conta_favorecido
            ),

            "tipo_conta_favorecido": (
                tipo_conta_favorecido
            ),

            "tipo_pessoa_favorecido": "",

            "nome": (
                nome_destinatario
            ),

            "cpf_cnpj": "",

            "valor": valor,

            "data_pagamento": (
                self._formatar_data(
                    data_pagamento
                )
            ),

            "autenticacao": ""

        }

    def _processar_segmento_b(
        self,
        linha
    ):

        if not self.pagamento_atual:

            return

        tipo_inscricao = (
            linha[17:18].strip()
        )

        numero_inscricao = (
            linha[18:33].strip()
        )

        self.pagamento_atual[
            "cpf_cnpj"
        ] = self._formatar_cpf_cnpj(
            tipo_inscricao,
            numero_inscricao
        )

        self.pagamento_atual[
            "tipo_pessoa_favorecido"
        ] = self._obter_tipo_pessoa(
            tipo_inscricao
        )

    def _processar_segmento_z(
        self,
        linha
    ):

        if not self.pagamento_atual:

            return

        autenticacao = (
            linha[78:103].strip()
        )

        self.pagamento_atual[
            "autenticacao"
        ] = autenticacao

    def _finalizar_pagamento(
        self
    ):

        if self.pagamento_atual:

            self.pagamentos.append(
                self.pagamento_atual
            )

            self.pagamento_atual = None

    @staticmethod
    def _converter_valor(
        valor
    ):

        valor = valor.strip()

        if not valor:

            return None

        try:

            return float(

                Decimal(valor)
                /
                Decimal("100")

            )

        except (
            InvalidOperation,
            ValueError
        ):

            return None

    @staticmethod
    def _formatar_data(
        data
    ):

        data = data.strip()

        if len(data) != 8:

            return data

        return (
            f"{data[0:2]}/"
            f"{data[2:4]}/"
            f"{data[4:8]}"
        )

    @staticmethod
    def _formatar_documento(
        tipo,
        documento
    ):

        documento = documento.strip()

        if tipo == "1":

            return documento.zfill(
                11
            )

        if tipo == "2":

            return documento.zfill(
                14
            )

        return documento

    @staticmethod
    def _formatar_cpf_cnpj(
        tipo,
        documento
    ):

        documento = CNAB240Parser._formatar_documento(
            tipo,
            documento
        )

        if tipo == "1" and len(documento) == 11:

            return (
                f"{documento[0:3]}."
                f"{documento[3:6]}."
                f"{documento[6:9]}-"
                f"{documento[9:11]}"
            )

        if tipo == "2" and len(documento) == 14:

            return (
                f"{documento[0:2]}."
                f"{documento[2:5]}."
                f"{documento[5:8]}/"
                f"{documento[8:12]}-"
                f"{documento[12:14]}"
            )

        return documento

    @staticmethod
    def _obter_nome_banco(
        codigo_banco
    ):

        bancos = {
            "033": "Banco Santander (Brasil) S.A."
        }

        return bancos.get(
            codigo_banco,
            ""
        )

    @staticmethod
    def _obter_tipo_pessoa(
        tipo_inscricao
    ):

        if tipo_inscricao == "1":

            return "Física"

        if tipo_inscricao == "2":

            return "Jurídica"

        return ""


def ler_arquivo_retorno(
    caminho_arquivo
):

    parser = CNAB240Parser(
        caminho_arquivo
    )

    return parser.parse()
