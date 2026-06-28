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
from services.erp_service import ErpService
from models.movimentacoes import Movimentacao


# Cria o objeto de banco de dados.
database = Database()
# Cria as tabelas do sistema caso ainda não existam.
# Isso garante que produtos, movimentações e solicitações estejam disponíveis no SQLite.
database.criar_tabelas()
# Serviço usado para exportar produtos, movimentações e solicitações em JSON.
json_export_service = JsonExportService()
# Serviço usado para simular integração com ERP utilizando exportação de dados.
erp_service = ErpService()

# Repository de produtos.
# Usado para salvar, listar, atualizar e excluir produtos no banco.
produto_repository = ProdutoRepository()
# Repository de solicitações de compra.
# Usado para consultar as solicitações geradas pelo sistema.
solicitacao_repository = SolicitacaoRepository()
# Repository de movimentações.
# Usado para consultar movimentações entre setores.
movimentacao_repository = MovimentacaoRepository()
# Serviço de estoque.
# Usado para verificar se um produto precisa de reposição.
estoque_service = EstoqueService()

# Cria um fornecedor padrão para receber as solicitações de orçamento.
# Quando o Almoxarifado precisa comprar produtos, esse fornecedor recebe o e-mail.
fornecedor = Fornecedor(
    "Yruan",
    "projeto.unisc.testes@gmail.com",
    "(51) 991789272"
)

# Função responsável por padronizar a escolha do setor.
# Em vez do usuário digitar "TI" ou "Almoxarifado", ele escolhe uma opção numérica.
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

# Função responsável por cadastrar um novo produto no sistema.
# Ela coleta os dados no terminal, cria um objeto Produto e salva esse produto no banco através do ProdutoRepository.
def cadastrar_produto():
    print("\n=== CADASTRAR PRODUTO ===")

    codigo = produto_repository.gerar_proximo_codigo_geral()

    print(f"Código gerado automaticamente: {codigo}")

    nome = input("Nome: ")
    preco = ler_float("Preço: ")

    print("\n--- Dados para o setor TI ---")
    quantidade_ti = ler_inteiro("Quantidade atual TI: ")
    estoque_minimo_ti = ler_inteiro("Estoque mínimo TI: ")
    estoque_maximo_ti = ler_inteiro("Estoque máximo TI: ")

    if estoque_maximo_ti < estoque_minimo_ti:
        print("Erro: o estoque máximo do TI não pode ser menor que o mínimo.")
        return

    print("\n--- Dados para o Almoxarifado ---")
    quantidade_almoxarifado = ler_inteiro("Quantidade atual Almoxarifado: ")
    estoque_minimo_almoxarifado = ler_inteiro("Estoque mínimo Almoxarifado: ")
    estoque_maximo_almoxarifado = ler_inteiro("Estoque máximo Almoxarifado: ")

    if estoque_maximo_almoxarifado < estoque_minimo_almoxarifado:
        print("Erro: o estoque máximo do Almoxarifado não pode ser menor que o mínimo.")
        return

    produto_ti = Produto(
        codigo,
        nome,
        quantidade_ti,
        preco,
        estoque_minimo_ti,
        estoque_maximo_ti
    )

    produto_almoxarifado = Produto(
        codigo,
        nome,
        quantidade_almoxarifado,
        preco,
        estoque_minimo_almoxarifado,
        estoque_maximo_almoxarifado
    )

    produto_repository.salvar(produto_ti, "TI")
    produto_repository.salvar(produto_almoxarifado, "Almoxarifado")

    print("\nProduto cadastrado com sucesso nos setores TI e Almoxarifado.")

#Ao cadastrar produto, verifique um código disponível automaticamente sem precisar ser manual    
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

# Função responsável por listar produtos de um setor específico.
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
            # Polimorfismo:
            # O sistema chama exibir_informacoes() sem precisar saber os detalhes internos da classe Produto.
            produto.exibir_informacoes()
            print("--------------------")

# Função responsável por listar todos os produtos cadastrados, independentemente do setor.
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

# Função responsável por atualizar somente a quantidade de um produto.
def atualizar_produto():
    print("\n=== ATUALIZAR QUANTIDADE ===")

    codigo = ler_inteiro("Código do produto: ")
    setor = selecionar_setor()

    if setor is None:
        return
    nova_quantidade = ler_inteiro("Nova quantidade: ")

    produto_repository.atualizar_quantidade(
        codigo,
        setor,
        nova_quantidade
    )
# Função responsável por excluir um produto do banco.
def excluir_produto():
    print("\n=== EXCLUIR PRODUTO ===")

    codigo = ler_inteiro("Código do produto: ")
    # Remove o produto do banco.
    produto_repository.excluir_por_codigo(codigo)
    
# Função responsável por listar todas as solicitações de compra.
# Ela utiliza o SolicitacaoRepository para buscar os registros salvos no banco.
def listar_solicitacoes():
    print("\n=== SOLICITAÇÕES DE COMPRA ===")

    # Busca todas as solicitações cadastradas no SQLite.
    solicitacoes = solicitacao_repository.listar_todas()
    # Verifica se não existem solicitações de compra cadastradas.
    if len(solicitacoes) == 0:
        print("Nenhuma solicitação encontrada.")
        return

    # Percorre todas as solicitações retornadas pelo banco.
    # Cada solicitação vem como uma tupla, por isso acessamos por índice.
    for solicitacao in solicitacoes:
        print(f"Número: {solicitacao[0]}")
        print(f"Código do Produto: {solicitacao[1]}")
        print(f"Produto: {solicitacao[2]}")
        print(f"Quantidade: {solicitacao[3]}")
        print(f"Fornecedor: {solicitacao[4]}")
        print(f"Status: {solicitacao[5]}")
        print(f"Data: {solicitacao[6]}")
        print("--------------------")

# Função responsável por registrar a retirada de um item para uso.
# O sistema baixa o estoque do setor e, se necessário, solicita complemento ao Almoxarifado.
def solicitar_item_para_uso():
    print("\n=== SOLICITAR ITEM PARA USO ===")

    codigo = ler_inteiro("Código do produto: ")
    setor = selecionar_setor()

    if setor is None:
        return
    quantidade_solicitada = ler_inteiro("Quantidade que será retirada para uso: ")

    produtos_setor = produto_repository.listar_por_setor(setor)

    produto_encontrado = None

    # Percorre todos os produtos do setor procurando pelo código informado.
    for produto in produtos_setor:
        if produto.get_codigo() == codigo:
            produto_encontrado = produto
            break

    if produto_encontrado is None:
        print("Produto não encontrado nesse setor.")
        return

    quantidade_disponivel_setor = produto_encontrado.get_quantidade()

    # Caso o setor tenha quantidade suficiente para atender toda a solicitação.
    if quantidade_disponivel_setor >= quantidade_solicitada:
        # Remove a quantidade solicitada do estoque do setor.
        produto_encontrado.remover_estoque(quantidade_solicitada)
        # Salva a nova quantidade no banco.
        produto_repository.salvar(produto_encontrado, setor)

        registrar_saida_para_uso(
            setor,
            produto_encontrado,
            quantidade_solicitada
        )

        print("\nItem retirado com sucesso.")
        print("Estoque atualizado:")
        produto_encontrado.exibir_informacoes()

        if setor == "TI":
            executar_reposicao_automatica(codigo)
        elif setor == "Almoxarifado":
            verificar_compra_almoxarifado(codigo)
    # Caso o setor não tenha quantidade suficiente.
    else:
        # Calcula quanto falta para atender totalmente a solicitação.
        quantidade_faltante = quantidade_solicitada - quantidade_disponivel_setor
        # Se quem está retirando é o próprio Almoxarifado,
        # não faz sentido solicitar ao Almoxarifado.
        if setor == "Almoxarifado":
            print("\nAlmoxarifado não possui quantidade suficiente para atender essa retirada.")
            print(f"Quantidade disponível: {quantidade_disponivel_setor}")
            print(f"Quantidade solicitada: {quantidade_solicitada}")

            verificar_compra_almoxarifado(codigo)
            return
        
        print("\nEstoque do setor não possui quantidade suficiente.")
        print(f"Quantidade disponível no {setor}: {quantidade_disponivel_setor}")
        print(f"Quantidade faltante: {quantidade_faltante}")
        print("Solicitando complemento ao Almoxarifado...")

        # Solicita ao Almoxarifado apenas a quantidade faltante.
        executar_reposicao_manual(codigo, setor, quantidade_faltante)

        # Após a tentativa de reposição, busca novamente os produtos do setor para obter as quantidades atualizadas.
        produtos_setor_atualizados = produto_repository.listar_por_setor(setor)
        # Variável para armazenar o produto depois da reposição.
        produto_atualizado = None

        # Procura novamente o produto pelo código.
        for produto in produtos_setor_atualizados:
            if produto.get_codigo() == codigo:
                produto_atualizado = produto
                break
        # Se por algum motivo o produto não for encontrado após a reposição, encerra o processo.
        if produto_atualizado is None:
            print("Produto não encontrado após reposição.")
            return

        # Verifica se, após pedir complemento ao Almoxarifado, o setor agora possui quantidade suficiente para atender a solicitação.
        if produto_atualizado.get_quantidade() >= quantidade_solicitada:
            # Remove a quantidade solicitada do estoque do setor.
            produto_atualizado.remover_estoque(quantidade_solicitada)
            # Salva a nova quantidade atualizada no banco.
            produto_repository.salvar(produto_atualizado, setor)

            print("\nItem atendido após reposição do Almoxarifado.")
            print("Estoque atualizado:")
            produto_atualizado.exibir_informacoes()

            # Após a retirada, verifica novamente se precisa repor o estoque.
            executar_reposicao_automatica(codigo)
        # Caso mesmo com a ajuda do Almoxarifado não tenha sido possível
        # atender a quantidade solicitada.
        else:
            print("\nMesmo após solicitar ao Almoxarifado, não há quantidade suficiente para atender totalmente.")
            print(f"Quantidade atual disponível no {setor}: {produto_atualizado.get_quantidade()}")

# Função responsável por verificar automaticamente se o TI precisa de reposição.
# Ela carrega os produtos do banco, monta os objetos TI e Almoxarifado, executa a regra de reposição e salva as novas quantidades no banco.
def executar_reposicao_automatica(codigo_produto):
    # Busca no banco todos os produtos do TI.
    produtos_ti = produto_repository.listar_por_setor("TI")
    # Busca no banco todos os produtos do Almoxarifado.
    produtos_almoxarifado = produto_repository.listar_por_setor("Almoxarifado")

    # Cria um objeto TI temporário para executar a regra de negócio.
    ti = TI()
    # Cria um objeto Almoxarifado temporário, vinculado ao fornecedor.
    almoxarifado = Almoxarifado(fornecedor)

    # Adiciona ao objeto TI todos os produtos carregados do banco.
    for produto in produtos_ti:
        ti.adicionar_produto(produto)

    # Adiciona ao objeto Almoxarifado todos os produtos carregados do banco.
    for produto in produtos_almoxarifado:
        almoxarifado.adicionar_produto(produto)

    # Executa a regra de estoque:
    # verifica se o produto está abaixo do mínimo e, se necessário, solicita reposição ao Almoxarifado.
    estoque_service.verificar_e_repor(
        ti,
        almoxarifado,
        codigo_produto
    )

    # Busca o produto específico no TI após a reposição.
    produto_ti = ti.buscar_produto_por_codigo(codigo_produto)
    # Busca o produto específico no Almoxarifado após a reposição.
    produto_almoxarifado = almoxarifado.buscar_produto_por_codigo(codigo_produto)

    # Se o produto existir no TI, salva sua quantidade atualizada no banco.
    if produto_ti is not None:
        produto_repository.salvar(produto_ti, "TI")

    # Se o produto existir no Almoxarifado, salva sua quantidade atualizada no banco.
    if produto_almoxarifado is not None:
        produto_repository.salvar(produto_almoxarifado, "Almoxarifado")
    
# Função responsável por solicitar manualmente uma quantidade específica ao Almoxarifado.
# Ela é usada quando o setor não possui quantidade suficiente para atender uma retirada.
def executar_reposicao_manual(codigo_produto, setor_destino, quantidade_necessaria):
    # Busca os produtos do setor que está precisando do complemento.
    produtos_setor = produto_repository.listar_por_setor(setor_destino)
    # Busca os produtos existentes no Almoxarifado.
    produtos_almoxarifado = produto_repository.listar_por_setor("Almoxarifado")

    ti = TI()
    almoxarifado = Almoxarifado(fornecedor)

    # Carrega no objeto TI os produtos vindos do setor solicitante.
    for produto in produtos_setor:
        ti.adicionar_produto(produto)

    # Adiciona no objeto almoxarifado todos os produtos carregados do banco
    for produto in produtos_almoxarifado:
        almoxarifado.adicionar_produto(produto)

    #Solicita ao Almoxarifado a quantidade necessária para completar a retirada do setor solicitante.
    almoxarifado.atender_solicitacao(
        ti,
        codigo_produto,
        quantidade_necessaria
    )

    # Busca o produto atualizado no setor após a reposição.
    produto_setor = ti.buscar_produto_por_codigo(codigo_produto)
    # Busca o produto atualizado no Almoxarifado após a reposição.
    produto_almoxarifado = almoxarifado.buscar_produto_por_codigo(codigo_produto)

    # Salva no banco a nova quantidade do produto no setor solicitante.
    if produto_setor is not None:
        produto_repository.salvar(produto_setor, setor_destino)

    # Salva no banco a nova quantidade do produto no Almoxarifado.
    if produto_almoxarifado is not None:
        produto_repository.salvar(produto_almoxarifado, "Almoxarifado")
       
# Função responsável por exportar os dados do sistema para arquivos JSON.
# Essa funcionalidade ajuda na integração com outros sistemas.        
def exportar_dados_json():
    print("\n=== EXPORTAR DADOS PARA JSON ===")

    # Busca todos os produtos cadastrados no banco.
    # Busca todas as movimentações registradas.
    # Busca todas as solicitações de compra registradas.
    produtos = produto_repository.listar_todos()
    movimentacoes = movimentacao_repository.listar_todas()
    solicitacoes = solicitacao_repository.listar_todas()

    # Exporta os produtos para produtos.json.
    # Exporta as movimentações para movimentacoes.json.
    # Exporta as solicitações para solicitacoes.json.
    json_export_service.exportar_produtos(produtos)
    json_export_service.exportar_movimentacoes(movimentacoes)
    json_export_service.exportar_solicitacoes(solicitacoes)

    print("\nArquivos gerados na pasta 'exportacoes'.")

# Função responsável por listar todas as movimentações no terminal.
def listar_movimentacoes():
    print("\n=== MOVIMENTAÇÕES ===")

    # Consulta todas as movimentações no banco.
    movimentacoes = movimentacao_repository.listar_todas()

    # Caso não exista nenhuma movimentação registrada.
    if len(movimentacoes) == 0:
        print("Nenhuma movimentação encontrada.")
        return

    # Percorre as movimentações e exibe os dados.
    # Cada movimentação vem como uma tupla retornada pelo banco.
    for movimentacao in movimentacoes:
        print(f"Número: {movimentacao[0]}")
        print(f"Origem: {movimentacao[1]}")
        print(f"Destino: {movimentacao[2]}")
        print(f"Código do Produto: {movimentacao[3]}")
        print(f"Produto: {movimentacao[4]}")
        print(f"Quantidade: {movimentacao[5]}")
        print(f"Data: {movimentacao[6]}")
        print("--------------------")

# Função responsável por simular a integração com ERP.
# Ela busca dados do banco e envia para o ErpService.
def integrar_com_erp():
    print("\n=== EXPORTAÇÃO PARA ERP ===")

    # Busca todos os dados necessários para a integração.
    produtos = produto_repository.listar_todos()
    movimentacoes = movimentacao_repository.listar_todas()
    solicitacoes = solicitacao_repository.listar_todas()

    # Envia os dados para o ErpService.
    # Atualmente o ErpService exporta esses dados em JSON, simulando a integração com um ERP externo.
    erp_service.exportar_dados_para_erp(
        produtos,
        movimentacoes,
        solicitacoes
    )

# Função auxiliar para ler números inteiros com segurança.
# Evita que o sistema quebre caso o usuário digite texto.
def ler_inteiro(mensagem):
    while True:
        try:
            # Tenta converter a entrada do usuário para inteiro.
            valor = int(input(mensagem))

            # Impede números negativos.
            if valor < 0:
                print("Digite um número maior ou igual a zero.")
            else:
                return valor
        # Caso o usuário digite algo que não seja número inteiro.
        except ValueError:
            print("Valor inválido. Digite um número inteiro.")
 
# Função auxiliar para ler números decimais com segurança.
# Usada principalmente para preços.           
def ler_float(mensagem):
    while True:
        try:
            # Tenta converter a entrada para número decimal.
            valor = float(input(mensagem))
            # Impede valores negativos.
            if valor < 0:
                print("Digite um valor maior ou igual a zero.")
            else:
                return valor
        # Caso o usuário digite algo inválido.
        except ValueError:
            print("Valor inválido. Digite um número válido.")
            
def registrar_saida_para_uso(setor_origem, produto, quantidade):
    numero = movimentacao_repository.gerar_proximo_numero()

    movimentacao = Movimentacao(
        numero,
        setor_origem,
        "Uso interno",
        produto,
        quantidade
    )

    movimentacao_repository.salvar(movimentacao)
    
def verificar_compra_almoxarifado(codigo_produto):
    produtos_almoxarifado = produto_repository.listar_por_setor("Almoxarifado")

    almoxarifado = Almoxarifado(fornecedor)

    for produto in produtos_almoxarifado:
        almoxarifado.adicionar_produto(produto)

    produto_almoxarifado = almoxarifado.buscar_produto_por_codigo(codigo_produto)

    if produto_almoxarifado is not None:
        almoxarifado.verificar_necessidade_compra(produto_almoxarifado)
        produto_repository.salvar(produto_almoxarifado, "Almoxarifado")


#MENU DE EXIBIÇÃO E SELEÇÃO
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
        print("10 - Integrar com ERP")
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
        elif opcao == "10":
            integrar_com_erp()
        else:
            print("Opção inválida.")

exibir_menu()