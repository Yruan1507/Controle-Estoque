#Classe responsável por toda persistência de solicitação de compra
#Responsabilidades: Salvar uma solicitação no banco, gerar próximo numero de solicitação, listar todas solicitações
#Se conecta com: Almoxarifado, Fornecedor (esse cria a solicitação), SolicitacaoCompra, SolicitacaoRepository, Database, SQLite e usado em main, API FASTAPI, ERP Simulado, JSONExportService e ERPService

from repositories.database import Database


class SolicitacaoRepository:

    def __init__(self):
        self.__database = Database()

    # Salva uma solicitação de compra no banco.
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

    # Gera automaticamente o próximo número da solicitação de compra.
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
    
    # Retorna todas as solicitações cadastradas ordenadas pela data de criação.
    def listar_todas(self):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT numero,
                   produto_codigo,
                   produto_nome,
                   quantidade,
                   fornecedor_nome,
                   status,
                   data_criacao
            FROM solicitacoes_compra
            ORDER BY data_criacao DESC
        """)

        registros = cursor.fetchall()

        conexao.close()

        return registros
    
"""A classe SolicitacaoRepository implementa a camada de persistência das solicitações de compra. Ela é responsável por gerar automaticamente a numeração das solicitações, armazenar os dados no banco SQLite e recuperar todas as solicitações cadastradas. Dessa forma, a lógica de negócio permanece nas classes Fornecedor e Almoxarifado, enquanto o acesso ao banco fica centralizado no Repository, mantendo a arquitetura organizada e com baixo acoplamento."""