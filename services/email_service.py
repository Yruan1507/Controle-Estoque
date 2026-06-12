import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class EmailService:

    def __init__(self):
        self.__email_remetente = os.getenv("EMAIL_REMETENTE")
        self.__senha_app = os.getenv("EMAIL_SENHA_APP")

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

        mensagem = EmailMessage()
        mensagem["From"] = self.__email_remetente
        mensagem["To"] = fornecedor.get_email()
        mensagem["Subject"] = assunto
        mensagem.set_content(corpo)

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(self.__email_remetente, self.__senha_app)
            smtp.send_message(mensagem)

        print("\nE-mail enviado com sucesso ao fornecedor.")