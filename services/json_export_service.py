import json
import os


class JsonExportService:

    def __init__(self):
        self.__pasta_exportacoes = "exportacoes"

        if not os.path.exists(self.__pasta_exportacoes):
            os.makedirs(self.__pasta_exportacoes)

    def exportar_produtos(self, produtos):
        caminho = os.path.join(self.__pasta_exportacoes, "produtos.json")

        dados = []

        for produto in produtos:
            dados.append({
                "codigo": produto[0],
                "nome": produto[1],
                "quantidade": produto[2],
                "preco": produto[3],
                "estoque_minimo": produto[4],
                "estoque_maximo": produto[5],
                "setor": produto[6]
            })

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        print("Produtos exportados com sucesso.")

    def exportar_movimentacoes(self, movimentacoes):
        caminho = os.path.join(self.__pasta_exportacoes, "movimentacoes.json")

        dados = []

        for movimentacao in movimentacoes:
            dados.append({
                "numero": movimentacao[0],
                "origem": movimentacao[1],
                "destino": movimentacao[2],
                "produto_codigo": movimentacao[3],
                "produto_nome": movimentacao[4],
                "quantidade": movimentacao[5],
                "data": movimentacao[6]
            })

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        print("Movimentações exportadas com sucesso.")

    def exportar_solicitacoes(self, solicitacoes):
        caminho = os.path.join(self.__pasta_exportacoes, "solicitacoes.json")

        dados = []

        for solicitacao in solicitacoes:
            dados.append({
                "numero": solicitacao[0],
                "produto_codigo": solicitacao[1],
                "produto_nome": solicitacao[2],
                "quantidade": solicitacao[3],
                "fornecedor": solicitacao[4],
                "status": solicitacao[5],
                "data_criacao": solicitacao[6]
            })

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        print("Solicitações exportadas com sucesso.")