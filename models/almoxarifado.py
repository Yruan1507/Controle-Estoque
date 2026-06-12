from models.setor import Setor


class Almoxarifado(Setor):

    def __init__(self, fornecedor):
        super().__init__("Almoxarifado")
        self.__fornecedor = fornecedor

    def atender_solicitacao(self, setor_solicitante, codigo_produto, quantidade):
        produto_almoxarifado = self.buscar_produto_por_codigo(codigo_produto)

        if produto_almoxarifado is None:
            print("\nAlmoxarifado não possui esse produto.")
            print("Não foi possível solicitar orçamento porque o produto não existe no almoxarifado.")
            return

        produto_setor = setor_solicitante.buscar_produto_por_codigo(codigo_produto)

        if produto_almoxarifado.get_quantidade() >= quantidade:
            produto_almoxarifado.remover_estoque(quantidade)
            produto_setor.adicionar_estoque(quantidade)

            print(f"\nAlmoxarifado enviou {quantidade} unidade(s) para {setor_solicitante.get_nome()}.")

        else:
            quantidade_disponivel = produto_almoxarifado.get_quantidade()

            if quantidade_disponivel > 0:
                produto_almoxarifado.remover_estoque(quantidade_disponivel)
                produto_setor.adicionar_estoque(quantidade_disponivel)

                print(f"\nAlmoxarifado enviou {quantidade_disponivel} unidade(s) para {setor_solicitante.get_nome()}.")

            quantidade_para_compra = produto_almoxarifado.quantidade_para_repor()

            print("\nAlmoxarifado não possui quantidade suficiente para atender tudo.")
            print(f"Quantidade disponível enviada: {quantidade_disponivel}")
            print(f"Quantidade necessária para completar o estoque máximo do almoxarifado: {quantidade_para_compra}")

            self.__fornecedor.solicitar_orcamento(
                produto_almoxarifado,
                quantidade_para_compra
            )

    def gerar_relatorio(self):
        print("\nRelatório específico do Almoxarifado")
        print("Controle geral de estoque industrial e reposições...")
        self.listar_produtos()