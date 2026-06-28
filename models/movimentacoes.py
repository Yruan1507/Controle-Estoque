# Representa uma transferência de um produto entre dois setores.

from datetime import datetime

# Classe responsável por representar uma movimentação de estoque
class Movimentacao:

    #CONSTRUTOR
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

    # Imprime as informações da Movimentação de produto nos setores
    def exibir_detalhes(self):
        print("\n===== MOVIMENTAÇÃO =====")
        print(f"Número: {self.__numero}")
        print(f"Origem: {self.__origem}")
        print(f"Destino: {self.__destino}")
        print(f"Produto: {self.__produto.get_nome()}")
        print(f"Quantidade: {self.__quantidade}")
        print(f"Data: {self.__data.strftime('%d/%m/%Y %H:%M')}")
        
        
        """"A classe Movimentacao representa cada transferência de produtos entre setores do sistema. Sempre que um item é enviado do Almoxarifado para outro setor, como o TI, é criado um objeto dessa classe contendo origem, destino, produto, quantidade e data da movimentação. A classe utiliza encapsulamento por meio de atributos privados e mantém uma associação com a classe Produto, armazenando o objeto do produto movimentado. Posteriormente, essas informações são persistidas no banco de dados pelo MovimentacaoRepository e disponibilizadas tanto pela API quanto pela exportação em JSON."
        """