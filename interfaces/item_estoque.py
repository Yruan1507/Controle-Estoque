# Importa os recursos necessários para criar uma classe abstrata
from abc import ABC, abstractmethod

# Classe abstrata que representa um item genérico de estoque
# Nenhum objeto desta classe pode ser criado diretamente
# Ela serve apenas como modelo para outras classes
class ItemEstoque(ABC):

    # Método abstrato
    # Toda classe que herdar de ItemEstoque será obrigada a possuir este método
    # Todo item de estoque precisa exibir suas informações - Abstração
    @abstractmethod
    def exibir_informacoes(self):
        pass
    
# Quem herda desta classe: Produto

# A classe ItemEstoque é uma classe abstrata que representa o conceito genérico de um item de estoque. 
# Ela implementa o princípio da Abstração, obrigando qualquer classe que a herde, como Produto, 
# a implementar o método exibir_informacoes(). Dessa forma, garantimos que todos os itens do sistema 
# possuam um comportamento padrão para exibição de informações, mantendo a organização e 
# facilitando futuras expansões do sistema.