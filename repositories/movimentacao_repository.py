from repositories.database import Database


class MovimentacaoRepository:

    def __init__(self):
        self.__database = Database()

    def gerar_proximo_numero(self):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT numero
            FROM movimentacoes
            ORDER BY numero DESC
            LIMIT 1
        """)

        resultado = cursor.fetchone()
        conexao.close()

        if resultado is None:
            return "MOV-0001"

        ultimo_numero = resultado[0]
        numero_inteiro = int(ultimo_numero.replace("MOV-", ""))
        proximo_numero = numero_inteiro + 1

        return f"MOV-{proximo_numero:04d}"

    def salvar(self, movimentacao):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO movimentacoes (
                numero,
                origem,
                destino,
                produto_codigo,
                produto_nome,
                quantidade,
                data
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            movimentacao.get_numero(),
            movimentacao.get_origem(),
            movimentacao.get_destino(),
            movimentacao.get_produto().get_codigo(),
            movimentacao.get_produto().get_nome(),
            movimentacao.get_quantidade(),
            movimentacao.get_data().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conexao.commit()
        conexao.close()

        print(f"Movimentação {movimentacao.get_numero()} salva no banco.")
        
    def listar_todas(self):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT numero,
                   origem,
                   destino,
                   produto_codigo,
                   produto_nome,
                   quantidade,
                   data
            FROM movimentacoes
            ORDER BY data DESC
        """)

        registros = cursor.fetchall()

        conexao.close()

        return registros