from repositories.database import Database
from models.produto import Produto


class ProdutoRepository:

    def __init__(self):
        self.__database = Database()

    def salvar(self, produto, setor):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

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

    def excluir(self, codigo, setor):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            DELETE FROM produtos
            WHERE codigo = ? AND setor = ?
        """, (
            codigo,
            setor
        ))

        conexao.commit()
        conexao.close()

        print("Produto removido com sucesso.")