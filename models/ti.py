from models.setor import Setor

#Representa o setor que consome os materiais
#A classe se conecta com Setor, Produto e Almoxarifado
#Classe TI ja herda da classe Setor
class TI(Setor):

    def __init__(self):
        #chamando o construtor da classe pai (Setor)
        #o objeto TI já surge com nome: TI e produtos
        super().__init__("TI")

    #Procura o produto no TI
    def verificar_reposicao(self, almoxarifado, codigo_produto):
        produto_ti = self.buscar_produto_por_codigo(codigo_produto)

        if produto_ti is None:
            print("Produto não encontrado no estoque do TI.")
            return

        #Verifica se está abaixo do estoque mínimo
        if produto_ti.estoque_abaixo_minimo():
            #Se estiver abaixo, verifica quanto falta para chegar no máximo
            quantidade_necessaria = produto_ti.quantidade_para_repor()

            print(f"\nEstoque baixo no TI para o produto: {produto_ti.get_nome()}")
            print(f"Quantidade necessária para reposição: {quantidade_necessaria}")

            #Chama o almoxarifado
            almoxarifado.atender_solicitacao(self, codigo_produto, quantidade_necessaria)
        else:
            print("\nEstoque do TI está dentro do limite.")

    def gerar_relatorio(self):
        print("\nRelatório específico do TI")
        print("Verificando equipamentos e periféricos em estoque...")
        self.listar_produtos()
        
"""A classe TI representa o setor de Tecnologia da Informação da empresa. Ela herda da classe Setor, reutilizando funcionalidades comuns como cadastro, listagem e busca de produtos. Sua principal responsabilidade é verificar se algum produto está abaixo do estoque mínimo e, quando necessário, solicitar automaticamente a reposição ao Almoxarifado. Além da Herança, essa classe demonstra Polimorfismo ao sobrescrever o método gerar_relatorio, produzindo um relatório específico para o setor de TI."""