#Essa classe é responsável por verificar se um setor precisa de reposição de estoque e, caso necessário, solicitar essa reposição ao Almoxarifado.
#Se conecta com: Produto, Setor, EstoqueService, Almoxarifado, Fornecedor
#Verificar necessidade de reposição e solicitar ao Almoxarifado.

class EstoqueService:

    # Verifica se um produto está abaixo do estoque mínimo.
    # Caso esteja, calcula a quantidade necessária e solicita reposição ao Almoxarifado.
    def verificar_e_repor(self, setor_solicitante, almoxarifado, codigo_produto):
        produto_setor = setor_solicitante.buscar_produto_por_codigo(codigo_produto)

        if produto_setor is None:
            print(f"\nProduto não encontrado no setor {setor_solicitante.get_nome()}.")
            return

        if produto_setor.estoque_abaixo_minimo():
            quantidade_necessaria = produto_setor.quantidade_para_repor()

            print(f"\nEstoque baixo no setor {setor_solicitante.get_nome()}.")
            print(f"Produto: {produto_setor.get_nome()}")
            print(f"Quantidade necessária: {quantidade_necessaria}")

            almoxarifado.atender_solicitacao(
                setor_solicitante,
                codigo_produto,
                quantidade_necessaria
            )
        else:
            print(f"\nEstoque do setor {setor_solicitante.get_nome()} está dentro do limite.")
            
"""A classe EstoqueService representa a camada de serviços responsável pelas regras de reposição de estoque. Ela verifica se um produto está abaixo do estoque mínimo, calcula automaticamente a quantidade necessária para reposição e solicita ao Almoxarifado o envio do material. Essa separação evita que essa regra fique espalhada pelas classes de domínio e facilita futuras manutenções."""