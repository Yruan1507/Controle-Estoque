#Responsável por fazer a ponte entre os objetos Produto e a tabela produtos do banco
#Se conecta com: Produto, ProdutoRepository, Database e SQLite, usado no main, api, JSONExportService e ERPService

from repositories.database import Database
from models.produto import Produto


class ProdutoRepository:

    def __init__(self):
        self.__database = Database()
    #Recebe um objeto Produto e o setor ao qual ele pertence
    def salvar(self, produto, setor):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        #Se não existir insere, senão, atualiza
        cursor.execute("""
            INSERT OR REPLACE INTO produtos (
                codigo,
                nome,
                quantidade,
                preco,
                estoque_minimo,
                estoque_maximo,
                setor
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            produto.get_codigo(),
            produto.get_nome(),
            produto.get_quantidade(),
            produto.get_preco(),
            produto.get_estoque_minimo(),
            produto.get_estoque_maximo(),
            setor
        ))

        conexao.commit()
        conexao.close()

        print(f"Produto {produto.get_nome()} salvo no banco para o setor {setor}.")

    #Lista todos os produtos por setor
    def listar_por_setor(self, setor):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT codigo, nome, quantidade, preco, estoque_minimo, estoque_maximo
            FROM produtos
            WHERE setor = ?
        """, (setor,))

        registros = cursor.fetchall()

        conexao.close()

        produtos = []

        for registro in registros:
            produto = Produto(
                registro[0],
                registro[1],
                registro[2],
                registro[3],
                registro[4],
                registro[5]
            )

            produtos.append(produto)

        return produtos
    
    #Lista todos produtos de todos setores
    def listar_todos(self):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT codigo,
                   nome,
                   quantidade,
                   preco,
                   estoque_minimo,
                   estoque_maximo,
                   setor
            FROM produtos
            ORDER BY setor, nome
        """)

        registros = cursor.fetchall()

        conexao.close()

        return registros

    #Atualiza quantidade de um produto específico
    def atualizar_quantidade(self, codigo, setor, nova_quantidade):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE produtos
            SET quantidade = ?
            WHERE codigo = ? AND setor = ?
        """, (
            nova_quantidade,
            codigo,
            setor
        ))

        conexao.commit()
        conexao.close()

        print("Quantidade atualizada com sucesso.")
        
    def gerar_proximo_codigo(self, setor):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT MAX(codigo)
            FROM produtos
            WHERE setor = ?
        """, (setor,))

        resultado = cursor.fetchone()

        conexao.close()

        if resultado[0] is None:
            return 1

        return resultado[0] + 1
    
    #Esse método busca o maior código existente em todos os setores e soma +1
    def gerar_proximo_codigo_geral(self):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT MAX(codigo)
            FROM produtos
        """)

        resultado = cursor.fetchone()
        conexao.close()

        if resultado[0] is None:
            return 1

        return resultado[0] + 1
    
    #Remove um produto do banco usando código e setor como referência
    def excluir_por_codigo(self, codigo):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            DELETE FROM produtos
            WHERE codigo = ?
        """, (codigo,))

        quantidade_removida = cursor.rowcount

        if quantidade_removida == 0:
            print("Produto não encontrado. Nenhum item foi removido.")
        else:
            conexao.commit()
            print(f"Produto removido com sucesso dos setores. Registros removidos: {quantidade_removida}")

        conexao.close()
        
"""A classe ProdutoRepository representa a camada de persistência dos produtos. Ela é responsável por salvar, consultar, atualizar e excluir produtos no banco SQLite. Essa separação evita que a classe Produto tenha comandos SQL, mantendo a regra de negócio separada do acesso ao banco. Além disso, o repository permite que o mesmo produto exista em setores diferentes, utilizando a combinação de código e setor como chave de identificação."""