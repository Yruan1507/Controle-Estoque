# Importa a classe principal do FastAPI.
# Ela será responsável por criar a API REST do sistema.
from fastapi import FastAPI
# Importa os Repositories responsáveis por consultar os dados diretamente no banco de dados SQLite.
from repositories.produto_repository import ProdutoRepository
from repositories.movimentacao_repository import MovimentacaoRepository
from repositories.solicitacao_repository import SolicitacaoRepository

# Cria a aplicação FastAPI.
# Essas informações aparecem automaticamente na documentação gerada pelo Swagger (http://localhost:8000/docs).
app = FastAPI(
    # Nome da API
    title="Smart Stock API",
    # Descrição exibida na documentação
    description="API de integração do sistema Smart Stock",
    version="1.0.0"
)

# Cria uma instância de cada Repository.
# Essas classes serão utilizadas para consultar os dados armazenados no banco SQLite.
produto_repository = ProdutoRepository()
movimentacao_repository = MovimentacaoRepository()
solicitacao_repository = SolicitacaoRepository()



# Endpoint principal da API.
# Quando alguém acessar: http://localhost:8000/ esta função será executada.
@app.get("/")
def home():
    # Retorna um JSON simples indicando que a API está funcionando.
    return {
        "sistema": "Smart Stock",
        "status": "online"
    }

# Endpoint responsável por listar todos os produtos.
# URL: http://localhost:8000/produtos
# Método HTTP: GET
@app.get("/produtos")
def listar_produtos():
    # Consulta todos os produtos cadastrados através do ProdutoRepository.
    produtos = produto_repository.listar_todos()

    # Lista que armazenará os produtos convertidos para JSON.
    resultado = []

    # Percorre todos os produtos retornados pelo banco.
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
    # Retorna o JSON para quem chamou a API.
    return resultado

# Endpoint responsável por listar todas as movimentações do estoque.
# URL: http://localhost:8000/movimentacoes
@app.get("/movimentacoes")
def listar_movimentacoes():
    # Consulta as movimentações no banco.
    movimentacoes = movimentacao_repository.listar_todas()

    resultado = []
    # Converte cada movimentação para JSON.
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

# Endpoint responsável por listar todas as solicitações de compra.
# URL: http://localhost:8000/solicitacoes
@app.get("/solicitacoes")
def listar_solicitacoes():
    # Consulta as solicitações cadastradas no banco.
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
    # O FastAPI devolve automaticamente essa lista em formato JSON.
    return resultado


"""Essa classe implementa a API REST do Smart Stock utilizando o framework FastAPI. Ela disponibiliza os dados do sistema através de endpoints HTTP, permitindo que aplicações externas consultem produtos, movimentações e solicitações de compra sem acessar diretamente o banco de dados. Cada endpoint utiliza um Repository para consultar o SQLite e retorna os dados em formato JSON, que é o padrão utilizado na comunicação entre sistemas."""