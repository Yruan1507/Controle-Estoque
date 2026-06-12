from models.produto import Produto
from repositories.database import Database
from repositories.produto_repository import ProdutoRepository
from models.ti import TI
from models.almoxarifado import Almoxarifado
from models.fornecedor import Fornecedor
from services.estoque_service import EstoqueService


database = Database()
database.criar_tabelas()

produto_repository = ProdutoRepository()
estoque_service = EstoqueService()

fornecedor = Fornecedor(
    "Yruan",
    "projeto.unisc.testes@gmail.com",
    "(51) 991789272"
)


def cadastrar_produto():
    print("\n=== CADASTRAR PRODUTO ===")

    codigo = int(input("Código: "))
    nome = input("Nome: ")
    quantidade = int(input("Quantidade: "))
    preco = float(input("Preço: "))
    estoque_minimo = int(input("Estoque mínimo: "))
    estoque_maximo = int(input("Estoque máximo: "))
    setor = input("Setor (TI ou Almoxarifado): ")

    produto = Produto(
        codigo,
        nome,
        quantidade,
        preco,
        estoque_minimo,
        estoque_maximo
    )

    produto_repository.salvar(produto, setor)


def listar_produtos():
    print("\n=== LISTAR PRODUTOS ===")
    setor = input("Informe o setor (TI ou Almoxarifado): ")

    produtos = produto_repository.listar_por_setor(setor)

    if len(produtos) == 0:
        print("Nenhum produto encontrado.")
    else:
        for produto in produtos:
            produto.exibir_informacoes()
            print("--------------------")

def listar_todos_produtos():

    print("\n=== TODOS OS PRODUTOS ===")

    produtos = produto_repository.listar_todos()

    if len(produtos) == 0:
        print("Nenhum produto encontrado.")
        return

    for produto in produtos:
        print(f"Setor: {produto[6]}")
        print(f"Código: {produto[0]}")
        print(f"Nome: {produto[1]}")
        print(f"Quantidade: {produto[2]}")
        print(f"Preço: R$ {produto[3]}")
        print("--------------------")

def atualizar_produto():
    print("\n=== ATUALIZAR QUANTIDADE ===")

    codigo = int(input("Código do produto: "))
    setor = input("Setor (TI ou Almoxarifado): ")
    nova_quantidade = int(input("Nova quantidade: "))

    produto_repository.atualizar_quantidade(
        codigo,
        setor,
        nova_quantidade
    )

def excluir_produto():
    print("\n=== EXCLUIR PRODUTO ===")

    codigo = int(input("Código do produto: "))
    setor = input("Setor (TI ou Almoxarifado): ")

    produto_repository.excluir(
        codigo,
        setor
    )

def solicitar_item_para_uso():
    print("\n=== SOLICITAR ITEM PARA USO ===")

    codigo = int(input("Código do produto: "))
    setor = input("Setor que vai utilizar o item (TI): ")
    quantidade_retirada = int(input("Quantidade que será retirada para uso: "))

    produtos_setor = produto_repository.listar_por_setor(setor)

    produto_encontrado = None

    for produto in produtos_setor:
        if produto.get_codigo() == codigo:
            produto_encontrado = produto
            break

    if produto_encontrado is None:
        print("Produto não encontrado nesse setor.")
        return

    if produto_encontrado.remover_estoque(quantidade_retirada):
        produto_repository.salvar(produto_encontrado, setor)

        print("\nItem retirado com sucesso.")
        print("Estoque atualizado:")
        produto_encontrado.exibir_informacoes()

        executar_reposicao_automatica(codigo)

def executar_reposicao_automatica(codigo_produto):
    produtos_ti = produto_repository.listar_por_setor("TI")
    produtos_almoxarifado = produto_repository.listar_por_setor("Almoxarifado")

    ti = TI()
    almoxarifado = Almoxarifado(fornecedor)

    for produto in produtos_ti:
        ti.adicionar_produto(produto)

    for produto in produtos_almoxarifado:
        almoxarifado.adicionar_produto(produto)

    estoque_service.verificar_e_repor(
        ti,
        almoxarifado,
        codigo_produto
    )

    produtos_ti_atualizados = ti.get_produtos()
    produtos_almoxarifado_atualizados = almoxarifado.get_produtos()

    for produto in produtos_ti_atualizados:
        produto_repository.salvar(produto, "TI")

    for produto in produtos_almoxarifado_atualizados:
        produto_repository.salvar(produto, "Almoxarifado")

def exibir_menu():
    while True:
        print("\n==============================")
        print(" SISTEMA DE CONTROLE DE ESTOQUE")
        print("==============================")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos por setor")
        print("3 - Listar todos os produtos")
        print("4 - Atualizar quantidade")
        print("5 - Excluir produto")
        print("6 - Solicitar item para uso")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "0":
            print("Sistema encerrado.")
            break
        elif opcao == "3":
            listar_todos_produtos()
        elif opcao == "4":
            atualizar_produto()
        elif opcao == "5":
            excluir_produto()
        elif opcao == "6":
            solicitar_item_para_uso()
        else:
            print("Opção inválida.")

exibir_menu()