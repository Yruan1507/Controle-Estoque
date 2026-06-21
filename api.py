from fastapi import FastAPI
from repositories.produto_repository import ProdutoRepository
from repositories.movimentacao_repository import MovimentacaoRepository
from repositories.solicitacao_repository import SolicitacaoRepository

app = FastAPI(
    title="Smart Stock API",
    description="API de integração do sistema Smart Stock",
    version="1.0.0"
)

produto_repository = ProdutoRepository()
movimentacao_repository = MovimentacaoRepository()
solicitacao_repository = SolicitacaoRepository()


@app.get("/")
def home():
    return {
        "sistema": "Smart Stock",
        "status": "online"
    }


@app.get("/produtos")
def listar_produtos():

    produtos = produto_repository.listar_todos()

    resultado = []

    for produto in produtos:
        resultado.append({
            "codigo": produto[0],
            "nome": produto[1],
            "quantidade": produto[2],
            "preco": produto[3],
            "estoque_minimo": produto[4],
            "estoque_maximo": produto[5],
            "setor": produto[6]
        })

    return resultado

@app.get("/movimentacoes")
def listar_movimentacoes():
    movimentacoes = movimentacao_repository.listar_todas()

    resultado = []

    for movimentacao in movimentacoes:
        resultado.append({
            "numero": movimentacao[0],
            "origem": movimentacao[1],
            "destino": movimentacao[2],
            "produto_codigo": movimentacao[3],
            "produto_nome": movimentacao[4],
            "quantidade": movimentacao[5],
            "data": movimentacao[6]
        })

    return resultado

@app.get("/solicitacoes")
def listar_solicitacoes():
    solicitacoes = solicitacao_repository.listar_todas()

    resultado = []

    for solicitacao in solicitacoes:
        resultado.append({
            "numero": solicitacao[0],
            "produto_codigo": solicitacao[1],
            "produto_nome": solicitacao[2],
            "quantidade": solicitacao[3],
            "fornecedor": solicitacao[4],
            "status": solicitacao[5],
            "data_criacao": solicitacao[6]
        })

    return resultado



#EXPLICAR
#"O Smart Stock disponibiliza seus dados através de uma API REST utilizando FastAPI, 
# permitindo que ERPs, aplicações web e outros sistemas consultem produtos, movimentações e solicitações de compra 
# através de endpoints HTTP."
#Sistema Externo
#      ↓
#    API REST
#       ↓
# Smart Stock
#       ↓
#   SQLite