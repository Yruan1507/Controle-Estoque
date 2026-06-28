# Se conecta com as classes TI, Almoxarifado e Produto

#Herança
#Quem herda é TI e Almoxarifado
class Setor:

    def __init__(self, nome):
        #Encapsulamento
        #Os atributos são privados.
        #Ninguém altera diretamente a lista de produtos.
        #Quem manipula essa lista são os métodos da própria classe.
        self.__nome = nome
        self.__produtos = []

    def get_nome(self):
        return self.__nome

    #Sempre que algum setor recebe um produto, eles utiliza:
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
    #Tudo passa por esse método, é usado pelo almoxarifado, EstoqueService, Main, Solicitação de Uso
    def buscar_produto_por_codigo(self, codigo):
        for produto in self.__produtos:
            #Verifica se produto existe
            if produto.get_codigo() == codigo:
                return produto

        return None

    def gerar_relatorio(self):
        print(f"\nRelatório padrão do setor {self.__nome}")
        self.listar_produtos()

    def get_produtos(self):
        return self.__produtos
    
""""A classe Setor representa um setor genérico da empresa e foi criada para evitar duplicação de código. Ela implementa funcionalidades comuns, como armazenar produtos, adicionar novos itens, listar o estoque e buscar produtos pelo código. As classes TI e Almoxarifado herdam dessa classe, reutilizando esses comportamentos. Dessa forma, aplicamos Herança para compartilhar funcionalidades, Encapsulamento por meio de atributos privados e Polimorfismo ao permitir que diferentes tipos de produtos sejam manipulados através do método exibir_informacoes() sem que a classe Setor conheça sua implementação específica."""