#Essa classe representa a camada de integração do Smart Stock com um ERP externo.
#Exporta dados em formato JSON
#Se conecta com: ProdutoRepository, MovimentacaoRepository, SolicitacaoRepository, ERP Service, JSONExportService, ERP Simulado e Arquivos JSON
#Preparar os dados para integração com um ERP.

from services.json_export_service import JsonExportService

class ErpService:
    # Inicializa o serviço de exportação em JSON.
    def __init__(self):
        self.__json_export_service = JsonExportService()
    
    # Exporta produtos, movimentações e solicitações para arquivos JSON utilizados na integração.
    def exportar_dados_para_erp(self, produtos, movimentacoes, solicitacoes):
        print("\n=== INTEGRAÇÃO COM ERP ===")
        print("Preparando dados para integração...")

        self.__json_export_service.exportar_produtos(produtos)
        self.__json_export_service.exportar_movimentacoes(movimentacoes)
        self.__json_export_service.exportar_solicitacoes(solicitacoes)

        print("Dados exportados para integração com ERP.")
        print("Arquivos JSON disponíveis na pasta 'exportacoes'.")
        
"""A classe ErpService representa a camada de integração do Smart Stock com sistemas externos. Atualmente ela utiliza o JsonExportService para exportar produtos, movimentações e solicitações de compra em formato JSON, simulando a comunicação com um ERP. Essa separação foi criada para que, futuramente, seja possível substituir a exportação em JSON por chamadas diretas a APIs de sistemas."""