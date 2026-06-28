#Classe de acesso ao banco de dados
#Classe responsável por conectar com o banco, criar tabelas, centralizar o acesso ao banco
#Classes que se conectam: ProdutoRepository, MovimentacaoRepository, SolicitacaoRepository

#Importando SQLite - Banco de dados
import sqlite3


class Database:

    def __init__(self, nome_banco="controle_estoque.db"):
        #Encapsulamento
        self.__nome_banco = nome_banco

    #Abstração
    def conectar(self):
        #Cria e retorna uma conexão com o banco
        return sqlite3.connect(self.__nome_banco)

    #Método mais importante que prepara o banco
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
        
        
"""A classe Database centraliza toda a comunicação com o banco de dados SQLite. Ela é responsável por abrir conexões e criar automaticamente todas as tabelas necessárias para o funcionamento do sistema. Dessa forma, os repositórios não precisam conhecer detalhes de configuração do banco, apenas solicitam uma conexão através dessa classe. Isso melhora a organização do projeto e reduz o acoplamento entre as camadas."""