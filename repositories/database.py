import sqlite3


class Database:

    def __init__(self, nome_banco="controle_estoque.db"):
        self.__nome_banco = nome_banco

    def conectar(self):
        return sqlite3.connect(self.__nome_banco)

    def criar_tabelas(self):
        conexao = self.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                codigo INTEGER NOT NULL,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL,
                estoque_minimo INTEGER NOT NULL,
                estoque_maximo INTEGER NOT NULL,
                setor TEXT NOT NULL,
                PRIMARY KEY (codigo, setor)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fornecedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solicitacoes_compra (
                numero TEXT PRIMARY KEY,
                produto_codigo INTEGER NOT NULL,
                produto_nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                fornecedor_nome TEXT NOT NULL,
                status TEXT NOT NULL,
                data_criacao TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimentacoes (
                numero TEXT PRIMARY KEY,
                origem TEXT NOT NULL,
                destino TEXT NOT NULL,
                produto_codigo INTEGER NOT NULL,
                produto_nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                data TEXT NOT NULL
            )
        """)
        
        conexao.commit()
        conexao.close()