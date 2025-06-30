import operacoesbd as db
import mysql.connector
from time import sleep

def center(texto, comprimento, caractere):
    if (comprimento - len(texto)) % 2 == 0:
        return f"{int((comprimento - len(texto))/2) * str(caractere)}" + texto + f"{int((comprimento - len(texto))/2) * str(caractere)}"
    else:
        return f"{int((comprimento - len(texto))/2) * str(caractere)}" + texto + f"{int((comprimento - len(texto))/2) * str(caractere)}" + caractere

#Definindo as cores do menu                      
red = '\033[1;31m'
yellow = '\033[1;33m'
cyan = '\033[1;36m'
green = '\033[1;32m'
clean = '\033[0;0m'
blue = '\033[34m'
bright_magenta = '\033[1;35m'
magenta = '\033[1;35m'
white_bg_black = '\033[30;47m'   # Black text on white background
green_bg_black = '\033[30;42m'   # Black text on green background
blue_bg_black = '\033[30;44m'    # Black text on blue background

dicionario_manifestacao = {
    1: "reclamação",
    2: "sugestão",
    3: "elogio"
}

# Criação da conexão do banco de dados 
conn = db.criarConexao("localhost", "root", "12345", "ouvidoria")

def criarTabelaOuvidoria():
    sql = """
    CREATE TABLE IF NOT EXISTS ouvidoria (
        codigo INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100),
        categoria ENUM('reclamação', 'sugestão', 'elogio'),
        manifestação TEXT
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()


criarTabelaOuvidoria()
#Apresentação do menu
print(center("BEM VINDO À OUVIDORIA!",70,"-"))
def menu():
   while True:
        print("-" * 70)
        print(center("Ouvidoria", 70, "-"))
        print("-" * 70)
        print(
            f"{center(f"{green}[1]{clean}LISTAR MANIFESTAÇÕES",70," ")}"
            f'\n{center(f"{red}[2]{clean}LISTAR MANIFESTAÇÕES POR CATEGORIA", 70," ")}'
            f'\n{center(f"{cyan}[3]{clean}ADICIONAR MANIFESTAÇÃO", 70," ")}'
            f'\n{center(f"{yellow}[4]{clean}EXIBIR MANIFESTAÇÃO PELO CÓDIGO",70," ")}'
            f'\n{center(f"{magenta}[5]{clean}PROCURAR MANIFESTAÇÃO PELO CÓDIGO",70," ")}'
            f'\n{center(f"{blue}[6]{clean}REMOVER MANIFESTAÇÃO PELO CÓDIGO",70," ")}'
            f'\n{center(f"{bright_magenta}[7]{clean}FINALIZAR MENU",70," ")}'
            )
        
        opcao = "".join(input(f"DIGITE SUA ESCOLHA: ").split())
        print("-" * 70)
        # Verifica se a opção é válida
        if opcao not in "1234567":

            print(f'{red}ENTRADA INVÁLIDA. É PERMITIDO APENAS SELECIONAR ALGUMA OPÇÃO DO MENU!{clean}')

        elif opcao == "1":
            listar_todas_manifestacoes()

        elif opcao == "2":
            listar_manifestacoes_tipo()

        elif opcao == "3":
            adicionar_manifestacao()

        elif opcao == "4":
            exibir_quantidade_manifestacoes()

        elif opcao == "5":
            procurar_manifestacao()

        elif opcao == "6":
            remover_manifestacao()
            
        elif opcao == "7":
            print("Saindo do menu...")
            db.encerrarConexao(conn)
            break
        sleep(0.5)
#Função para registrar uma ouvidoria

def listar_todas_manifestacoes():
    
    sql = "SELECT codigo, nome, categoria, manifestação FROM ouvidoria"
    resultados = db.listarBancoDados(conn, sql)
    
    if len(resultados) == 0:
        print(f"{red}Nenhuma manifestação encontrada.{clean}")
        sleep(0.5)
        
    else:
        for ouvidoria in resultados:
            print(f"CODIGO: {ouvidoria[0]} {white_bg_black}  NOME: {ouvidoria[1]}  {green_bg_black}  CATEGORIA: {ouvidoria[2]}  {blue_bg_black}  MANIFESTAÇÃO: {ouvidoria[3]}  {clean}")
            sleep(0.5)

def listar_manifestacoes_tipo():
    while True:

        categoria = "".join(input(f"Categorias" 
                    f"\n{green}[1]{clean}reclamação" 
                    f"\n{red}[2]{clean}sugestão "
                    f"\n{cyan}[3]{clean}elogio: ").split())
    
        if categoria in "123":
            categoria = dicionario_manifestacao[int(categoria)]
            break
    
        else:
            print(f"{red}Categoria inválida. Por favor, escolha uma opção válida.{clean}")
            sleep(0.5)

    sql = f"SELECT codigo, nome, categoria, manifestação FROM ouvidoria WHERE categoria = '{categoria}'"
    resultados = db.listarBancoDados(conn, sql)
    
    if len(resultados) == 0:
        print(f"{red}Nenhuma {categoria} encontrada.{clean}")
        sleep(0.5)
        
    else:
        for ouvidoria in resultados:
            print(f"CODIGO: {ouvidoria[0]} {white_bg_black}  NOME: {ouvidoria[1]}  {blue_bg_black}  MANIFESTAÇÃO: {ouvidoria[3]}  {clean}")
            sleep(0.5)

def adicionar_manifestacao():
    
    nome = input("Digite seu nome: ")
    
    while True:

        categoria = "".join(input(f"Categorias" 
                    f"\n{green}[1]{clean}reclamação" 
                    f"\n{red}[2]{clean}sugestão "
                    f"\n{cyan}[3]{clean}elogio: ").split())
    
        if categoria in "123":
            categoria = dicionario_manifestacao[int(categoria)]
            break
  
        else:
            print(f"{red}Categoria inválida. Por favor, escolha uma opção válida.{clean}")
            sleep(0.5)

    manifestacao = input("Digite sua manifestação: ")
    print("\n")

    sql = "INSERT INTO ouvidoria (nome, categoria, manifestação) VALUES (%s, %s, %s)"
    dados = (nome, categoria, manifestacao)

    id = db.insertNoBancoDados(conn, sql, dados)
    if id:
        print("Manifestação registrada com sucesso.")
        sleep(0.5)
    else:
        print(f"{red}Erro ao registrar a manifestação.{clean}")
        sleep(0.5)


def remover_manifestacao():
    while True:    
        try:
            codigo_de_remocao = int("".join(input("Digite o código da manifestação a ser removida: ").split()))
            sleep(0.5)
            break
        
        except ValueError:
            print(f"{red}Por favor, insira um número inteiro para o código.{clean}")
            sleep(0.5)

    sql = "DELETE FROM ouvidoria WHERE codigo = %s"
    dados = (codigo_de_remocao,) 
    manifestacao_excluida = db.excluirBancoDados(conn, sql, dados)
    print(manifestacao_excluida)

    if manifestacao_excluida > 0:
        print(f"{green}Manifestação com código {codigo_de_remocao} removida com sucesso!{clean}")
        sleep(0.5)

    else:
        print(f"{red}Nenhuma manifestação encontrada com o código {codigo_de_remocao}.{clean}")
        sleep(0.5)

def exibir_quantidade_manifestacoes():
    consulta = 'select count(*) from ouvidoria'
    quantidade_de_manifestacoes = db.listarBancoDados(conn,consulta)
    print('Temos',quantidade_de_manifestacoes[0][0],'manifestação(s).')

#Função para procurar uma manifestacao por códigona 
def procurar_manifestacao():
    
    while True:    
        try:
            codigo = int("".join(input("Digite o código da manifestação a ser exibida: ").split()))
            sleep(0.5)
            break
            

        except ValueError:
            print(f"{red}Por favor, insira um número inteiro para o código.{clean}")
            sleep(0.5)

    sql = "SELECT * FROM ouvidoria WHERE codigo = %s"
    dados = (codigo,)
    resultados = db.listarBancoDados(conn, sql, dados)
    
    if len(resultados) > 0:
        for mensagem in resultados:
            print(f"Código: {mensagem[0]}\nNome: {mensagem[1]}\nCategoria: {mensagem[2]}\nManifestação: {mensagem[3]}")
        sleep(0.5)

    else:
        print(f"{red}Não existe manifestação com esse código.{clean}")
        sleep(0.5)

#Executando o programa
menu()
