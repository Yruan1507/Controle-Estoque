class EstoqueService:

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