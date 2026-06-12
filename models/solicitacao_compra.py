from datetime import datetime


class SolicitacaoCompra:

    def __init__(self, numero, produto, quantidade, fornecedor):
        self.__numero = numero
        self.__produto = produto
        self.__quantidade = quantidade
        self.__fornecedor = fornecedor
        self.__status = "AGUARDANDO ORCAMENTO"
        self.__data_criacao = datetime.now()

    def get_numero(self):
        return self.__numero

    def get_status(self):
        return self.__status

    def get_produto(self):
        return self.__produto

    def get_quantidade(self):
        return self.__quantidade

    def get_fornecedor(self):
        return self.__fornecedor

    def get_data_criacao(self):
        return self.__data_criacao

    def atualizar_status(self, novo_status):
        self.__status = novo_status

    def exibir_detalhes(self):
        print("\n===== SOLICITAÇÃO DE COMPRA =====")
        print(f"Número: {self.__numero}")
        print(f"Data: {self.__data_criacao.strftime('%d/%m/%Y %H:%M')}")
        print(f"Produto: {self.__produto.get_nome()}")
        print(f"Quantidade: {self.__quantidade}")
        print(f"Fornecedor: {self.__fornecedor.get_nome()}")
        print(f"Status: {self.__status}")