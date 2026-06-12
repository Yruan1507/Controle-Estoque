from models.solicitacao_compra import SolicitacaoCompra
from services.email_service import EmailService
from repositories.solicitacao_repository import SolicitacaoRepository

class Fornecedor:

    def __init__(self, nome, email, telefone):
        self.__nome = nome
        self.__email = email
        self.__telefone = telefone
        self.__solicitacoes = []
        self.__email_service = EmailService()
        self.__solicitacao_repository = SolicitacaoRepository()

    def get_nome(self):
        return self.__nome

    def get_email(self):
        return self.__email

    def solicitar_orcamento(self, produto, quantidade):
        numero = self.__solicitacao_repository.gerar_proximo_numero()

        solicitacao = SolicitacaoCompra(
            numero,
            produto,
            quantidade,
            self
        )

        self.__solicitacoes.append(solicitacao)
        self.__solicitacao_repository.salvar(solicitacao)

        print("\nSolicitação de orçamento criada:")
        solicitacao.exibir_detalhes()
        self.__email_service.enviar_solicitacao_orcamento(solicitacao)

    def listar_solicitacoes(self):
        print(f"\nSolicitações do fornecedor {self.__nome}:")

        if len(self.__solicitacoes) == 0:
            print("Nenhuma solicitação encontrada.")
        else:
            for solicitacao in self.__solicitacoes:
                solicitacao.exibir_detalhes()

    