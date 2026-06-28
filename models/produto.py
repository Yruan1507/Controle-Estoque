# Importa a interface ItemEstoque
# Produto herda dessa classe e é obrigado a implementar o método exibir_informacoes()

from interfaces.item_estoque import ItemEstoque

# Classe responsável por representar um produto do estoque
# Cada objeto Produto possui os dados abaixo
# Herda de ItemEstoque, demonstrando Herança
class Produto(ItemEstoque):
    #Contrutor
    #Inicializa atributos do produto
    def __init__(self, codigo, nome, quantidade, preco, estoque_minimo, estoque_maximo):
        self.__codigo = codigo
        self.__nome = nome
        self.__quantidade = quantidade
        self.__preco = preco
        self.__estoque_minimo = estoque_minimo
        self.__estoque_maximo = estoque_maximo

    # Métodos GET utilizados para acessar os atributos privados

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

    # Adiciona quantidade ao estoque do produto
    # Utilizado quando almoxarifado envia produto ao outro setor ou quanto contém reposição
    def adicionar_estoque(self, quantidade):
        if quantidade > 0:
            self.__quantidade += quantidade

    def remover_estoque(self, quantidade):
        #Antes de remover do estoque, verifica se contém quantidade suficiente
        if quantidade <= self.__quantidade:
            self.__quantidade -= quantidade
            return True
        else:
            print("Quantidade insuficiente em estoque.")
            return False

    #Verifica se estoque atual está abaixo do mínimo ou igual
    #Se sim, dispara reposição automática
    def estoque_abaixo_minimo(self):
        return self.__quantidade <= self.__estoque_minimo

    #Verifica quanto falta para o produto atingir novamente o estoque máximo
    #Valor é utilizado para solicitações de compra
    def quantidade_para_repor(self):
        return self.__estoque_maximo - self.__quantidade

    # Abstração e Polimorfismo
    # Método obrigatório herdado da classe ItemEstoque.
    def exibir_informacoes(self):
        print(f"Código: {self.__codigo}")
        print(f"Nome: {self.__nome}")
        print(f"Quantidade: {self.__quantidade}")
        print(f"Preço: R$ {self.__preco}")
        print(f"Estoque mínimo: {self.__estoque_minimo}")
        print(f"Estoque máximo: {self.__estoque_maximo}")
        

#############################################################
# POO presente nesta classe
#
# Herança:
# Produto herda da classe abstrata ItemEstoque.
#
# Encapsulamento:
# Todos os atributos são privados e acessados através dos
# métodos get.
#
# Abstração:
# Implementa o método exibir_informacoes() definido na
# interface ItemEstoque.
#
# Polimorfismo:
# O método exibir_informacoes() pode possuir implementações
# diferentes em outras classes que herdem de ItemEstoque.
#
# Responsabilidade:
# Representar um produto do estoque e controlar operações
# relacionadas à quantidade disponível.
#############################################################

        """"A classe Produto é a principal entidade do sistema, pois representa cada item controlado no estoque. Ela armazena informações como código, nome, quantidade disponível, preço, estoque mínimo e estoque máximo."

Depois continuaria:

"Além de armazenar os dados, ela também é responsável pelas operações relacionadas ao próprio produto, como adicionar itens ao estoque, remover itens, verificar se o estoque está abaixo do mínimo e calcular quanto precisa ser comprado para voltar ao estoque máximo."

Depois entraria na POO:

"Essa classe demonstra os quatro pilares da Programação Orientada a Objetos. Ela herda da classe abstrata ItemEstoque, caracterizando Herança e Abstração. Também utiliza Encapsulamento, pois todos os seus atributos são privados e acessados através de métodos getters. O método exibir_informacoes() implementa o comportamento definido na classe abstrata, demonstrando também Polimorfismo."

Por fim, faria a ligação com o restante do projeto:

"O objeto Produto é utilizado praticamente em todo o sistema. Ele é armazenado nos setores TI e Almoxarifado, salvo no banco de dados pelo ProdutoRepository, utilizado na criação de movimentações, nas solicitações de compra, na exportação para JSON e também é disponibilizado pela API FastAPI para integração com outros sistemas."

Se ela perguntar: "Por que você colocou esses métodos dentro do Produto?"

Você pode responder:

"Porque eles fazem parte da responsabilidade do próprio produto. Quem melhor sabe adicionar ou remover quantidade do estoque é o próprio objeto Produto. Dessa forma seguimos o princípio da responsabilidade única, deixando a lógica de negócio organizada e evitando que outras classes alterem diretamente a quantidade."

Essa resposta costuma impressionar bastante, porque demonstra que você entende o conceito de encapsulamento e responsabilidade dos objetos.

Se ela perguntar: "Por que usar uma classe Produto e não um dicionário?"

Você pode responder:

"Utilizando uma classe, conseguimos encapsular dados e comportamentos no mesmo objeto. Além das informações do produto, ele também sabe verificar se está abaixo do estoque mínimo, calcular a quantidade para reposição e controlar alterações de estoque. Isso torna o código mais organizado, reutilizável e facilita futuras manutenções."

A resposta que eu daria em uma banca (30 segundos)

"A classe Produto representa cada item do estoque e é a entidade central do sistema. Ela armazena as informações do produto e implementa operações relacionadas ao próprio estoque, como adicionar, remover, verificar estoque mínimo e calcular reposição. Ela demonstra os pilares da Programação Orientada a Objetos ao herdar de uma classe abstrata, utilizar encapsulamento com atributos privados e implementar um método obrigatório definido pela interface. Esse objeto é utilizado por praticamente todas as camadas do sistema, como setores, banco de dados, API e integração com ERP."
        """