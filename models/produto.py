from interfaces.item_estoque import ItemEstoque

class Produto(ItemEstoque):

    def __init__(self, codigo, nome, quantidade, preco, estoque_minimo, estoque_maximo):
        self.__codigo = codigo
        self.__nome = nome
        self.__quantidade = quantidade
        self.__preco = preco
        self.__estoque_minimo = estoque_minimo
        self.__estoque_maximo = estoque_maximo

    def get_codigo(self):
        return self.__codigo

    def get_nome(self):
        return self.__nome

    def get_quantidade(self):
        return self.__quantidade

    def get_preco(self):
        return self.__preco

    def get_estoque_minimo(self):
        return self.__estoque_minimo

    def get_estoque_maximo(self):
        return self.__estoque_maximo

    def adicionar_estoque(self, quantidade):
        self.__quantidade += quantidade

    def remover_estoque(self, quantidade):
        if quantidade <= self.__quantidade:
            self.__quantidade -= quantidade
            return True
        else:
            print("Quantidade insuficiente em estoque.")
            return False

    def estoque_abaixo_minimo(self):
        return self.__quantidade <= self.__estoque_minimo

    def quantidade_para_repor(self):
        return self.__estoque_maximo - self.__quantidade

    def exibir_informacoes(self):
        print(f"Código: {self.__codigo}")
        print(f"Nome: {self.__nome}")
        print(f"Quantidade: {self.__quantidade}")
        print(f"Preço: R$ {self.__preco}")
        print(f"Estoque mínimo: {self.__estoque_minimo}")
        print(f"Estoque máximo: {self.__estoque_maximo}")