from models.produto import Produto
from repositories.database import Database
from repositories.produto_repository import ProdutoRepository
from models.ti import TI
from models.almoxarifado import Almoxarifado
from models.fornecedor import Fornecedor
from services.estoque_service import EstoqueService
from repositories.movimentacao_repository import MovimentacaoRepository
from repositories.solicitacao_repository import SolicitacaoRepository
from services.json_export_service import JsonExportService



database = Database()
database.criar_tabelas()
json_export_service = JsonExportService()

produto_repository = ProdutoRepository()
solicitacao_repository = SolicitacaoRepository()
movimentacao_repository = MovimentacaoRepository()
estoque_service = EstoqueService()

fornecedor = Fornecedor(
    "Yruan",
    "projeto.unisc.testes@gmail.com",
    "(51) 991789272"
)


def selecionar_setor():
    print("\nSelecione o setor:")
    print("1 - TI")
    print("2 - Almoxarifado")

    opcao = input("Opção: ")

    if opcao == "1":
        return "TI"
    elif opcao == "2":
        return "Almoxarifado"
    else:
        print("Setor inválido.")
        return None

def cadastrar_produto():
    print("\n=== CADASTRAR PRODUTO ===")

    codigo = int(input("Código: "))
    nome = input("Nome: ")
    quantidade = int(input("Quantidade: "))
    preco = float(input("Preço: "))
    estoque_minimo = int(input("Estoque mínimo: "))
    estoque_maximo = int(input("Estoque máximo: "))
    
    setor = selecionar_setor()

    if setor is None:
        return

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

    setor = selecionar_setor()

    if setor is None:
        return

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
    setor = selecionar_setor()

    if setor is None:
        return
    nova_quantidade = int(input("Nova quantidade: "))

    produto_repository.atualizar_quantidade(
        codigo,
        setor,
        nova_quantidade
    )

def excluir_produto():
    print("\n=== EXCLUIR PRODUTO ===")

    codigo = int(input("Código do produto: "))
    setor = selecionar_setor()

    if setor is None:
        return

    produto_repository.excluir(
        codigo,
        setor
    )
    
def listar_solicitacoes():
    print("\n=== SOLICITAÇÕES DE COMPRA ===")

    solicitacoes = solicitacao_repository.listar_todas()

    if len(solicitacoes) == 0:
        print("Nenhuma solicitação encontrada.")
        return

    for solicitacao in solicitacoes:
        print(f"Número: {solicitacao[0]}")
        print(f"Código do Produto: {solicitacao[1]}")
        print(f"Produto: {solicitacao[2]}")
        print(f"Quantidade: {solicitacao[3]}")
        print(f"Fornecedor: {solicitacao[4]}")
        print(f"Status: {solicitacao[5]}")
        print(f"Data: {solicitacao[6]}")
        print("--------------------")

def solicitar_item_para_uso():
    print("\n=== SOLICITAR ITEM PARA USO ===")

    codigo = int(input("Código do produto: "))
    setor = selecionar_setor()

    if setor is None:
        return
    quantidade_solicitada = int(input("Quantidade que será retirada para uso: "))

    produtos_setor = produto_repository.listar_por_setor(setor)

    produto_encontrado = None

    for produto in produtos_setor:
        if produto.get_codigo() == codigo:
            produto_encontrado = produto
            break

    if produto_encontrado is None:
        print("Produto não encontrado nesse setor.")
        return

    quantidade_disponivel_setor = produto_encontrado.get_quantidade()

    if quantidade_disponivel_setor >= quantidade_solicitada:
        produto_encontrado.remover_estoque(quantidade_solicitada)
        produto_repository.salvar(produto_encontrado, setor)

        print("\nItem retirado com sucesso.")
        print("Estoque atualizado:")
        produto_encontrado.exibir_informacoes()

        executar_reposicao_automatica(codigo)

    else:
        quantidade_faltante = quantidade_solicitada - quantidade_disponivel_setor

        print("\nEstoque do setor não possui quantidade suficiente.")
        print(f"Quantidade disponível no {setor}: {quantidade_disponivel_setor}")
        print(f"Quantidade faltante: {quantidade_faltante}")
        print("Solicitando complemento ao Almoxarifado...")

        executar_reposicao_manual(codigo, setor, quantidade_faltante)

        produtos_setor_atualizados = produto_repository.listar_por_setor(setor)

        produto_atualizado = None

        for produto in produtos_setor_atualizados:
            if produto.get_codigo() == codigo:
                produto_atualizado = produto
                break

        if produto_atualizado is None:
            print("Produto não encontrado após reposição.")
            return

        if produto_atualizado.get_quantidade() >= quantidade_solicitada:
            produto_atualizado.remover_estoque(quantidade_solicitada)
            produto_repository.salvar(produto_atualizado, setor)

            print("\nItem atendido após reposição do Almoxarifado.")
            print("Estoque atualizado:")
            produto_atualizado.exibir_informacoes()

            executar_reposicao_automatica(codigo)
        else:
            print("\nMesmo após solicitar ao Almoxarifado, não há quantidade suficiente para atender totalmente.")
            print(f"Quantidade atual disponível no {setor}: {produto_atualizado.get_quantidade()}")

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

    produto_ti = ti.buscar_produto_por_codigo(codigo_produto)
    produto_almoxarifado = almoxarifado.buscar_produto_por_codigo(codigo_produto)

    if produto_ti is not None:
        produto_repository.salvar(produto_ti, "TI")

    if produto_almoxarifado is not None:
        produto_repository.salvar(produto_almoxarifado, "Almoxarifado")
        
def executar_reposicao_manual(codigo_produto, setor_destino, quantidade_necessaria):
    produtos_setor = produto_repository.listar_por_setor(setor_destino)
    produtos_almoxarifado = produto_repository.listar_por_setor("Almoxarifado")

    ti = TI()
    almoxarifado = Almoxarifado(fornecedor)

    for produto in produtos_setor:
        ti.adicionar_produto(produto)

    for produto in produtos_almoxarifado:
        almoxarifado.adicionar_produto(produto)

    almoxarifado.atender_solicitacao(
        ti,
        codigo_produto,
        quantidade_necessaria
    )

    produto_setor = ti.buscar_produto_por_codigo(codigo_produto)
    produto_almoxarifado = almoxarifado.buscar_produto_por_codigo(codigo_produto)

    if produto_setor is not None:
        produto_repository.salvar(produto_setor, setor_destino)

    if produto_almoxarifado is not None:
        produto_repository.salvar(produto_almoxarifado, "Almoxarifado")
        
def exportar_dados_json():
    print("\n=== EXPORTAR DADOS PARA JSON ===")

    produtos = produto_repository.listar_todos()
    movimentacoes = movimentacao_repository.listar_todas()
    solicitacoes = solicitacao_repository.listar_todas()

    json_export_service.exportar_produtos(produtos)
    json_export_service.exportar_movimentacoes(movimentacoes)
    json_export_service.exportar_solicitacoes(solicitacoes)

    print("\nArquivos gerados na pasta 'exportacoes'.")
        
def listar_movimentacoes():
    print("\n=== MOVIMENTAÇÕES ===")

    movimentacoes = movimentacao_repository.listar_todas()

    if len(movimentacoes) == 0:
        print("Nenhuma movimentação encontrada.")
        return

    for movimentacao in movimentacoes:
        print(f"Número: {movimentacao[0]}")
        print(f"Origem: {movimentacao[1]}")
        print(f"Destino: {movimentacao[2]}")
        print(f"Código do Produto: {movimentacao[3]}")
        print(f"Produto: {movimentacao[4]}")
        print(f"Quantidade: {movimentacao[5]}")
        print(f"Data: {movimentacao[6]}")
        print("--------------------")

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
        print("7 - Listar movimentações")
        print("8 - Listar solicitações de compra")
        print("9 - Exportar dados para JSON")
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
        elif opcao == "7":
            listar_movimentacoes()
        elif opcao == "8":
            listar_solicitacoes()
        elif opcao == "9":
            exportar_dados_json()
        else:
            print("Opção inválida.")

exibir_menu()