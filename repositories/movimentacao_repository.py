#Responsável por todas as operações relacionadas às movimentações no banco de dados.
#Responsabilidades: gerar próximo número de movimentação, salvar no banco, listar todas movimentações
#Se conecta com: Almoxarifado, Movimentacao, Database, SQLite, API FastAPI, ERP Simulado e Exportacao JSON

from repositories.database import Database

class MovimentacaoRepository:
    # Inicializa o Repository criando uma conexão com a classe Database
    def __init__(self):
        self.__database = Database()

    #Consulta o banco e gera o próximo número de movimentacao
    def gerar_proximo_numero(self):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT numero
            FROM movimentacoes
            ORDER BY numero DESC
            LIMIT 1
        """)

        resultado = cursor.fetchone()
        conexao.close()

        if resultado is None:
            return "MOV-0001"

        ultimo_numero = resultado[0]
        numero_inteiro = int(ultimo_numero.replace("MOV-", ""))
        proximo_numero = numero_inteiro + 1

        return f"MOV-{proximo_numero:04d}"

    #Método que pega um objeto movimentacao e transforma em um registro no SQLite
    def salvar(self, movimentacao):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO movimentacoes (
                numero,
                origem,
                destino,
                produto_codigo,
                produto_nome,
                quantidade,
                data
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            movimentacao.get_numero(),
            movimentacao.get_origem(),
            movimentacao.get_destino(),
            movimentacao.get_produto().get_codigo(),
            movimentacao.get_produto().get_nome(),
            movimentacao.get_quantidade(),
            movimentacao.get_data().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conexao.commit()
        conexao.close()

        print(f"Movimentação {movimentacao.get_numero()} salva no banco.")
        
    # Retorna movimentações cadastradas, ordenadas da mais recente para a mais antiga    
    def listar_todas(self):
        conexao = self.__database.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT numero,
                   origem,
                   destino,
                   produto_codigo,
                   produto_nome,
                   quantidade,
                   data
            FROM movimentacoes
            ORDER BY data DESC
        """)
        #fetchall = todas as linhas
        registros = cursor.fetchall()

        conexao.close()

        return registros
    
"""A classe MovimentacaoRepository implementa a camada de persistência das movimentações. Ela é responsável por gerar automaticamente a numeração das movimentações, salvar os registros no banco SQLite e consultar todas as movimentações cadastradas. Essa separação permite que a regra de negócio permaneça na classe Almoxarifado, enquanto o acesso ao banco fica centralizado no Repository, reduzindo o acoplamento e facilitando a manutenção do sistema."""