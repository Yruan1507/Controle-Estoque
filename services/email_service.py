#Biblioteca responsável por conversar com servidores SMTP
import smtplib
#Serve para acessar variaveis do sistema operacional
import os
#Permite montar email
from email.message import EmailMessage
from dotenv import load_dotenv
#Lê o arquivo .env para segurança
load_dotenv()

#Classe responsável por enviar email automático quando uma solicitação de compra é criada
#Recebe um objeto SolicitacaoCompra, monta uma mensagem com as informações da solicitação e utiliza o servidor SMTP do GMAIL para enviá-la ao fornecedor.
#Se conecta com Almoxarifado, Fornecedor, SolicitacaoCompra, EmailService

class EmailService:

    def __init__(self):
        #CONSTRUTOR
        #OBS.:Caso trocar a conta, só alterar no arquivo .env sem modificar o código
        self.__email_remetente = os.getenv("EMAIL_REMETENTE")
        self.__senha_app = os.getenv("EMAIL_SENHA_APP")

    #Faz tudo: Recebe solicitacaocompra, monta assunto, monta corpo do email, cria EmailMessage, conecta no gmail, faz login, envia e fecha conexão
    def enviar_solicitacao_orcamento(self, solicitacao):
        fornecedor = solicitacao.get_fornecedor()
        produto = solicitacao.get_produto()

        assunto = f"Solicitação de Orçamento - {solicitacao.get_numero()}"

        corpo = f"""
Olá {fornecedor.get_nome()},

Favor enviar orçamento para o item abaixo:

Número da solicitação: {solicitacao.get_numero()}
Data: {solicitacao.get_data_criacao().strftime('%d/%m/%Y %H:%M')}

Produto: {produto.get_nome()}
Quantidade: {solicitacao.get_quantidade()}

Atenciosamente,
Sistema Controle de Estoque
"""
        #EmailMessage serve para montar o e-mail
        mensagem = EmailMessage()
        mensagem["From"] = self.__email_remetente
        mensagem["To"] = fornecedor.get_email()
        mensagem["Subject"] = assunto
        mensagem.set_content(corpo)
        
        #O with abre a conexão e garante que ela será fechada automaticamente quando terminar.
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(self.__email_remetente, self.__senha_app)
            smtp.send_message(mensagem)

        print("\nE-mail enviado com sucesso ao fornecedor.")
        
"""A classe EmailService é responsável pelo envio automático de e-mails aos fornecedores. Quando uma solicitação de compra é criada, ela recebe um objeto SolicitacaoCompra, monta o assunto e o corpo da mensagem e utiliza o protocolo SMTP do Gmail para realizar o envio. As credenciais ficam armazenadas em um arquivo .env, evitando que informações sensíveis fiquem expostas no código. Dessa forma, a responsabilidade de comunicação por e-mail fica isolada em uma única classe, mantendo a arquitetura organizada."""