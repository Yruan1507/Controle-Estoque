from datetime import datetime


class Movimentacao:

    def __init__(self, numero, origem, destino, produto, quantidade):
        self.__numero = numero
        self.__origem = origem
        self.__destino = destino
        self.__produto = produto
        self.__quantidade = quantidade
        self.__data = datetime.now()

    def get_numero(self):
        return self.__numero

    def get_origem(self):
        return self.__origem

    def get_destino(self):
        return self.__destino

    def get_produto(self):
        return self.__produto

    def get_quantidade(self):
        return self.__quantidade

    def get_data(self):
        return self.__data

    def exibir_detalhes(self):
        print("\n===== MOVIMENTAÇÃO =====")
        print(f"Número: {self.__numero}")
        print(f"Origem: {self.__origem}")
        print(f"Destino: {self.__destino}")
        print(f"Produto: {self.__produto.get_nome()}")
        print(f"Quantidade: {self.__quantidade}")
        print(f"Data: {self.__data.strftime('%d/%m/%Y %H:%M')}")