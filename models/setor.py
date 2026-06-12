class Setor:

    def __init__(self, nome):
        self.__nome = nome
        self.__produtos = []

    def get_nome(self):
        return self.__nome

    def adicionar_produto(self, produto):
        self.__produtos.append(produto)

    def listar_produtos(self):
        print(f"\nProdutos do setor {self.__nome}:")

        if len(self.__produtos) == 0:
            print("Nenhum produto cadastrado.")
        else:
            for produto in self.__produtos:

                #Polimorfismo - O setor não precisa saber qual tipo de produto está recebendo
                produto.exibir_informacoes()
                print("--------------------")


    #Verifica se existe o produto no estoque
    def buscar_produto_por_codigo(self, codigo):
        for produto in self.__produtos:
            if produto.get_codigo() == codigo:
                return produto

        return None

    def gerar_relatorio(self):
        print(f"\nRelatório padrão do setor {self.__nome}")
        self.listar_produtos()

    def get_produtos(self):
        return self.__produtos