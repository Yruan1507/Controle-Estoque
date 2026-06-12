from repositories.database import Database


class SolicitacaoRepository:

    def __init__(self):
        self.__database = Database()

    def salvar(self, solicitacao):

        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO solicitacoes_compra (
                numero,
                produto_codigo,
                produto_nome,
                quantidade,
                fornecedor_nome,
                status,
                data_criacao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            solicitacao.get_numero(),
            solicitacao.get_produto().get_codigo(),
            solicitacao.get_produto().get_nome(),
            solicitacao.get_quantidade(),
            solicitacao.get_fornecedor().get_nome(),
            solicitacao.get_status(),
            solicitacao.get_data_criacao().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conexao.commit()
        conexao.close()

        print(
            f"Solicitação {solicitacao.get_numero()} salva no banco."
        )

    def gerar_proximo_numero(self):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT numero
            FROM solicitacoes_compra
            ORDER BY numero DESC
            LIMIT 1
        """)

        resultado = cursor.fetchone()
        conexao.close()

        if resultado is None:
            return "SC-0001"

        ultimo_numero = resultado[0]
        numero_inteiro = int(ultimo_numero.replace("SC-", ""))
        proximo_numero = numero_inteiro + 1

        return f"SC-{proximo_numero:04d}"