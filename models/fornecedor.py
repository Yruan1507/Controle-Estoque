# Importa a classe responsável por representar uma solicitação de compra
# Importa o serviço responsável pelo envio de e-mails
# Importa o repositório responsável por salvar e consultar solicitações
from models.solicitacao_compra import SolicitacaoCompra
from services.email_service import EmailService
from repositories.solicitacao_repository import SolicitacaoRepository

# Classe responsável por representar um fornecedor
# O fornecedor recebe solicitações de orçamento quando o estoque do almoxarifado precisa ser reposto
class Fornecedor:
    # Construtor da classe
    def __init__(self, nome, email, telefone):
        # Atributos privados do fornecedor
        # O uso de "__" representa encapsulamento
        self.__nome = nome
        self.__email = email
        self.__telefone = telefone
        # Lista que armazena as solicitações criadas durante a execução
        self.__solicitacoes = []
        # Serviço responsável por enviar e-mails
        self.__email_service = EmailService()
        # Repositório responsável por salvar solicitações no banco
        self.__solicitacao_repository = SolicitacaoRepository()

    # Retorna o nome do fornecedor
    def get_nome(self):
        return self.__nome

    # Retorna o e-mail do fornecedor
    def get_email(self):
        return self.__email

    # Método responsável por criar uma solicitação de orçamento quando o almoxarifado precisa comprar determinado produto
    def solicitar_orcamento(self, produto, quantidade):
        # Gera automaticamente o próximo número da solicitação
        numero = self.__solicitacao_repository.gerar_proximo_numero()

        # Cria um objeto Solicitação de Compra
        solicitacao = SolicitacaoCompra(
            numero,
            produto,
            quantidade,
            self
        )
        
        # Adiciona a solicitação na lista em memória
        self.__solicitacoes.append(solicitacao)
        # Salva a solicitação no banco de dados SQLite
        self.__solicitacao_repository.salvar(solicitacao)

        print("\nSolicitação de orçamento criada:")
        solicitacao.exibir_detalhes()
        # Envia um e-mail real com os dados da solicitação
        self.__email_service.enviar_solicitacao_orcamento(solicitacao)

    # Exibe todas as solicitações associadas ao fornecedor
    def listar_solicitacoes(self):
        print(f"\nSolicitações do fornecedor {self.__nome}:")

        # Verifica se existe alguma solicitação cadastrada
        if len(self.__solicitacoes) == 0:
            print("Nenhuma solicitação encontrada.")
            
        # Percorre a lista exibindo cada solicitação
        else:
            for solicitacao in self.__solicitacoes:
                solicitacao.exibir_detalhes()


###################################################
#Esse arquivo é muito importante porque ele conecta várias partes do sistema:

#Model (SolicitacaoCompra)
#Service (EmailService)
#Repository (SolicitacaoRepository)
#Banco de Dados
#E-mail

#FLUXO:
#Almoxarifado sem estoque
#↓
#Fornecedor.solicitar_orcamento()
#↓
#Cria SolicitaçãoCompra
#↓
#Salva no SQLite
#↓
#Exibe no terminal
#↓
#Envia e-mail real
###################################################