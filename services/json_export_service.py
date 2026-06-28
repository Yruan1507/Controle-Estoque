# Importa a biblioteca json, usada para transformar dados Python como listas e dicionários em arquivos no formato JSON.
import json
# Importa a biblioteca os, usada para trabalhar com caminhos, pastas e arquivos do sistema operacional.
import os

#essa classe faz parte da camada de Serviços (Services) e é responsável apenas por gerar arquivos JSON.
#gera 3 arquivos: produtos, movimentacoes e solicitacoes, todas em JSON
class JsonExportService:

    # Construtor da classe.
    # É executado automaticamente quando criamos um objeto JsonExportService.
    def __init__(self):
        # Define o nome da pasta onde os arquivos JSON serão salvos.
        # O uso de "__" indica encapsulamento, deixando o atributo privado.
        self.__pasta_exportacoes = "exportacoes"
        # Verifica se a pasta de exportações ainda não existe.
        # Caso não exista, o sistema cria automaticamente.
        # Isso evita erro ao tentar salvar arquivos dentro de uma pasta inexistente.
        if not os.path.exists(self.__pasta_exportacoes):
            os.makedirs(self.__pasta_exportacoes)

    # Método responsável por exportar os produtos para um arquivo JSON.
    # Ele recebe uma lista de produtos vinda do ProdutoRepository.
    def exportar_produtos(self, produtos):
        caminho = os.path.join(self.__pasta_exportacoes, "produtos.json")

        # Lista que armazenará os produtos no formato de dicionário.
        # Depois essa lista será convertida para JSON.
        dados = []

        # Percorre todos os produtos recebidos.
        # Cada produto vem como uma tupla retornada pelo banco de dados.
        for produto in produtos:
            dados.append({
                "codigo": produto[0],
                "nome": produto[1],
                "quantidade": produto[2],
                "preco": produto[3],
                "estoque_minimo": produto[4],
                "estoque_maximo": produto[5],
                "setor": produto[6]
            })

        # Abre ou cria o arquivo produtos.json no modo escrita.
        # encoding="utf-8" permite salvar acentos corretamente.
        # O with garante que o arquivo será fechado automaticamente.
        with open(caminho, "w", encoding="utf-8") as arquivo:
            # Converte a lista de dicionários para JSON e grava no arquivo.
            # ensure_ascii=False mantém caracteres especiais como ç e ã.
            # indent=4 deixa o arquivo formatado e mais fácil de ler.
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        print("Produtos exportados com sucesso.")

    # Método responsável por exportar as movimentações para JSON.
    # Movimentações representam transferências entre setores.
    def exportar_movimentacoes(self, movimentacoes):
        caminho = os.path.join(self.__pasta_exportacoes, "movimentacoes.json")

        dados = []

        # Percorre todas as movimentações vindas do banco.
        for movimentacao in movimentacoes:
            # Cada movimentação é transformada em um dicionário.
            dados.append({
                "numero": movimentacao[0],
                "origem": movimentacao[1],
                "destino": movimentacao[2],
                "produto_codigo": movimentacao[3],
                "produto_nome": movimentacao[4],
                "quantidade": movimentacao[5],
                "data": movimentacao[6]
            })

        # Cria ou sobrescreve o arquivo movimentacoes.json.
        with open(caminho, "w", encoding="utf-8") as arquivo:
            # Grava os dados no formato JSON.
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        print("Movimentações exportadas com sucesso.")

    # Método responsável por exportar as solicitações de compra para JSON.
    # Solicitações são geradas quando o Almoxarifado precisa comprar produtos.
    def exportar_solicitacoes(self, solicitacoes):
        caminho = os.path.join(self.__pasta_exportacoes, "solicitacoes.json")

        dados = []

        for solicitacao in solicitacoes:
            dados.append({
                "numero": solicitacao[0],
                "produto_codigo": solicitacao[1],
                "produto_nome": solicitacao[2],
                "quantidade": solicitacao[3],
                "fornecedor": solicitacao[4],
                "status": solicitacao[5],
                "data_criacao": solicitacao[6]
            })
        # Cria ou sobrescreve o arquivo solicitacoes.json.
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        print("Solicitações exportadas com sucesso.")
        
"""A classe JsonExportService é responsável por exportar os dados do sistema em formato JSON. Ela recebe informações de produtos, movimentações e solicitações de compra e gera arquivos estruturados que podem ser consumidos por outros sistemas. Essa funcionalidade foi criada para atender ao requisito de integração, permitindo que um ERP simulado ou qualquer outro software consiga importar os dados do Smart Stock sem acessar diretamente o banco de dados."""
