#Esse arquivo representa um segundo software.
#Ele não faz parte do Smart Stock.
#Ele apenas consulta as informações.
#É como se fosse um cliente da API.

# Importa a biblioteca requests.
# Essa biblioteca permite que o programa faça requisições HTTP, como se fosse um navegador acessando uma API.
import requests

# URL base da API do Smart Stock.
# Todas as consultas serão feitas a partir desse endereço.
# Como a API está rodando localmente, utiliza localhost (127.0.0.1) e a porta padrão do FastAPI (8000).
URL_BASE = "http://127.0.0.1:8000"

# Função responsável por consultar todos os produtos disponíveis na API do Smart Stock.
def consultar_produtos():
    print("\n=== ERP SIMULADO - PRODUTOS ===")

    # Realiza uma requisição HTTP GET para o endpoint /produtos.
    # A API responde com um JSON contendo todos os produtos.
    resposta = requests.get(f"{URL_BASE}/produtos")
    # Converte automaticamente o JSON recebido para uma lista de dicionários Python.
    produtos = resposta.json()

    # Percorre todos os produtos recebidos.
    for produto in produtos:
        print(f"Produto: {produto['nome']}")
        print(f"Setor: {produto['setor']}")
        print(f"Quantidade: {produto['quantidade']}")
        print("--------------------")

# Função responsável por consultar todas as movimentações de estoque.
def consultar_movimentacoes():
    print("\n=== ERP SIMULADO - MOVIMENTAÇÕES ===")

    # Faz uma requisição GET para o endpoint /movimentacoes.
    resposta = requests.get(f"{URL_BASE}/movimentacoes")
    # Converte o JSON retornado pela API.
    movimentacoes = resposta.json()

    # Percorre todas as movimentações recebidas.
    for movimentacao in movimentacoes:
        print(f"Número: {movimentacao['numero']}")
        print(f"Origem: {movimentacao['origem']}")
        print(f"Destino: {movimentacao['destino']}")
        print(f"Produto: {movimentacao['produto_nome']}")
        print(f"Quantidade: {movimentacao['quantidade']}")
        print(f"Data: {movimentacao['data']}")
        print("--------------------")

# Função responsável por consultar todas as solicitações de compra.
def consultar_solicitacoes():
    print("\n=== ERP SIMULADO - SOLICITAÇÕES DE COMPRA ===")

    # Realiza uma requisição GET para o endpoint /solicitacoes.
    # o requests.get() é quem faz a comunicação entre os dois sistemas.
    resposta = requests.get(f"{URL_BASE}/solicitacoes")
    # Converte o JSON recebido em objetos Python.
    solicitacoes = resposta.json()

    # Percorre todas as solicitações retornadas pela API.
    for solicitacao in solicitacoes:
        print(f"Número: {solicitacao['numero']}")
        print(f"Produto: {solicitacao['produto_nome']}")
        print(f"Quantidade: {solicitacao['quantidade']}")
        print(f"Fornecedor: {solicitacao['fornecedor']}")
        print(f"Status: {solicitacao['status']}")
        print(f"Data: {solicitacao['data_criacao']}")
        print("--------------------")

# Início da execução do ERP Simulado.
# Cada função consulta um endpoint diferente da API.
consultar_produtos()
consultar_movimentacoes()
consultar_solicitacoes()

"""Essa aplicação representa um ERP externo consumindo os dados do Smart Stock. Ela utiliza a biblioteca requests para realizar requisições HTTP à API REST desenvolvida em FastAPI. Cada função consulta um endpoint específico (/produtos, /movimentacoes e /solicitacoes), recebe os dados em formato JSON e os apresenta no terminal. Dessa forma, demonstramos que outro sistema consegue integrar-se ao Smart Stock sem acessar diretamente o banco de dados."""