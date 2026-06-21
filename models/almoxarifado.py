# Importa a classe Setor, que será a classe pai do Almoxarifado
from models.setor import Setor
from models.movimentacoes import Movimentacao
from repositories.movimentacao_repository import MovimentacaoRepository

# A classe Almoxarifado herda de Setor
# Ela reaproveita atributos e métodos da classe Setor, como adicionar_produto, listar_produtos e buscar_produto_por_codigo
class Almoxarifado(Setor):

    # Construtor da classe Almoxarifado
    # Recebe um fornecedor, pois caso o estoque não seja suficiente, o almoxarifado poderá solicitar orçamento automaticamente
    def __init__(self, fornecedor):
        # Chama o construtor da classe pai Setor
        # Define o nome do setor como "Almoxarifado"
        super().__init__("Almoxarifado")
        self.__fornecedor = fornecedor
        self.__movimentacao_repository = MovimentacaoRepository()

    # Método responsável por atender uma solicitação feita por outro setor, como o TI, por exemplo
    def atender_solicitacao(self, setor_solicitante, codigo_produto, quantidade):
        # Busca no estoque do almoxarifado o produto solicitado pelo código
        produto_almoxarifado = self.buscar_produto_por_codigo(codigo_produto)

        # Se o produto não existir no almoxarifado, não é possível atender, nem solicitar orçamento, pois não há referência do produto
        if produto_almoxarifado is None:
            print("\nAlmoxarifado não possui esse produto.")
            print("Não foi possível solicitar orçamento porque o produto não existe no almoxarifado.")
            return

        # Busca o mesmo produto no setor que fez a solicitação
        # Exemplo: busca o produto dentro do estoque do TI
        produto_setor = setor_solicitante.buscar_produto_por_codigo(codigo_produto)

        # Verifica se o almoxarifado possui quantidade suficiente para atender toda a solicitação
        if produto_almoxarifado.get_quantidade() >= quantidade:
            # Remove a quantidade do estoque do almoxarifado
            produto_almoxarifado.remover_estoque(quantidade)
            # Adiciona a quantidade ao estoque do setor solicitante
            produto_setor.adicionar_estoque(quantidade)
            
            self.registrar_movimentacao(
                setor_solicitante,
                produto_almoxarifado,
                quantidade
            )

            print(f"\nAlmoxarifado enviou {quantidade} unidade(s) para {setor_solicitante.get_nome()}.")
            self.verificar_necessidade_compra(produto_almoxarifado)

        # Caso o almoxarifado não tenha quantidade suficiente
        else:
            # Armazena a quantidade disponível no almoxarifado
            quantidade_disponivel = produto_almoxarifado.get_quantidade()

            # Se existir alguma quantidade disponível, o almoxarifado envia tudo o que possui
            if quantidade_disponivel > 0:
                # Remove todo o estoque disponível do almoxarifado
                produto_almoxarifado.remover_estoque(quantidade_disponivel)
                # Adiciona essa quantidade ao setor solicitante
                produto_setor.adicionar_estoque(quantidade_disponivel)
                
                self.registrar_movimentacao(
                    setor_solicitante,
                    produto_almoxarifado,
                    quantidade_disponivel
                )

                print(f"\nAlmoxarifado enviou {quantidade_disponivel} unidade(s) para {setor_solicitante.get_nome()}.")


            # Após enviar o que tinha, calcula quanto falta para o almoxarifado voltar ao seu estoque máximo
            quantidade_para_compra = produto_almoxarifado.quantidade_para_repor()

            print("\nAlmoxarifado não possui quantidade suficiente para atender tudo.")
            print(f"Quantidade disponível enviada: {quantidade_disponivel}")
            print(f"Quantidade necessária para completar o estoque máximo do almoxarifado: {quantidade_para_compra}")

            # Solicita orçamento ao fornecedor para repor o estoque do almoxarifado 
            self.__fornecedor.solicitar_orcamento(
                produto_almoxarifado,
                quantidade_para_compra
            )

    # Método sobrescrito para gerar um relatório específico do Almoxarifado
    # Esse método demonstra polimorfismo, pois existe também em outras classes, como TI, mas com comportamento diferente
    def gerar_relatorio(self):
        print("\nRelatório específico do Almoxarifado")
        print("Controle geral de estoque industrial e reposições...")
        self.listar_produtos()
        
    def registrar_movimentacao(self, destino, produto, quantidade):
        numero = self.__movimentacao_repository.gerar_proximo_numero()

        movimentacao = Movimentacao(
            numero,
            self.get_nome(),
            destino.get_nome(),
            produto,
            quantidade
        )

        self.__movimentacao_repository.salvar(movimentacao)
    
    def verificar_necessidade_compra(self, produto):
        if produto.estoque_abaixo_minimo():
            quantidade_para_compra = produto.quantidade_para_repor()

            print("\nEstoque do Almoxarifado abaixo do mínimo.")
            print(f"Produto: {produto.get_nome()}")
            print(f"Quantidade atual: {produto.get_quantidade()}")
            print(f"Quantidade para completar estoque máximo: {quantidade_para_compra}")

            self.__fornecedor.solicitar_orcamento(
                produto,
                quantidade_para_compra
            )

###############################################
#Herança:
#Almoxarifado herda de Setor.   

#Encapsulamento:
#O fornecedor fica privado em self.__fornecedor.

#Polimorfismo:
#O método gerar_relatorio() tem comportamento específico no Almoxarifado.

#Regra de negócio:
#O Almoxarifado atende o setor solicitante, envia o que possui e, se necessário,
#gera solicitação de orçamento ao fornecedor.
###############################################