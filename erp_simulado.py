import requests


URL_BASE = "http://127.0.0.1:8000"


def consultar_produtos():
    print("\n=== ERP SIMULADO - PRODUTOS ===")

    resposta = requests.get(f"{URL_BASE}/produtos")
    produtos = resposta.json()

    for produto in produtos:
        print(f"Produto: {produto['nome']}")
        print(f"Setor: {produto['setor']}")
        print(f"Quantidade: {produto['quantidade']}")
        print("--------------------")


def consultar_movimentacoes():
    print("\n=== ERP SIMULADO - MOVIMENTAÇÕES ===")

    resposta = requests.get(f"{URL_BASE}/movimentacoes")
    movimentacoes = resposta.json()

    for movimentacao in movimentacoes:
        print(f"Número: {movimentacao['numero']}")
        print(f"Origem: {movimentacao['origem']}")
        print(f"Destino: {movimentacao['destino']}")
        print(f"Produto: {movimentacao['produto_nome']}")
        print(f"Quantidade: {movimentacao['quantidade']}")
        print(f"Data: {movimentacao['data']}")
        print("--------------------")


def consultar_solicitacoes():
    print("\n=== ERP SIMULADO - SOLICITAÇÕES DE COMPRA ===")

    resposta = requests.get(f"{URL_BASE}/solicitacoes")
    solicitacoes = resposta.json()

    for solicitacao in solicitacoes:
        print(f"Número: {solicitacao['numero']}")
        print(f"Produto: {solicitacao['produto_nome']}")
        print(f"Quantidade: {solicitacao['quantidade']}")
        print(f"Fornecedor: {solicitacao['fornecedor']}")
        print(f"Status: {solicitacao['status']}")
        print(f"Data: {solicitacao['data_criacao']}")
        print("--------------------")


consultar_produtos()
consultar_movimentacoes()
consultar_solicitacoes()