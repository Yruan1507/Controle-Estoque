from abc import ABC, abstractmethod


class ItemEstoque(ABC):

    @abstractmethod
    def exibir_informacoes(self):
        pass