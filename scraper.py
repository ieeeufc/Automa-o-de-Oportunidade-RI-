import requests
from bs4 import BeautifulSoup 
import mysql.connector
from mysql.connector import Error

def testar_conexao():
    try:
        # Tenta estabelecer a ligação com o MariaDB local
        conexao = mysql.connector.connect(
            host='127.0.0.1',
            database='ieee_automacao',
            user= 'root',
            password= ''
        )

        if conexao.is_connected():
            print("Conexão bem-sucedida ao banco de dados MariaDB!")

            cursor = conexao.cursor()
            # Executa um comando SQL simples para ler 5 sociedades
            cursor.execute("SELECT sigla, nome_completo FROM sociedades LIMIT 5")
            registros = cursor.fetchall()

            print("Registros lidos do banco de dados:")
            for registro in registros:
                print(f"Sigla: {registro[0]}, Nome Completo: {registro[1]}")

    except Error as erro:
        print(f"Erro ao conectar ao banco de dados MariaDB: {erro}")

    finally:
        # Fecha a conexão com o banco de dados, se estiver aberta
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão com o banco de dados MariaDB fechada.")

def buscar_editais_reais(url_alvo, id_sociedade, categoria):
    print(f"\n--- Vasculhando: {url_alvo} ---")

    # 1. O requests baixa o código-fonte da página. O "User-Agent" evita que o site bloqueie o bot.
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    resposta = requests.get(url_alvo, headers=headers)

    # 2. O BeautifulSoup organiza o HTML num formato facilmente pesquisável pelo Python
    site = BeautifulSoup(resposta.text, 'html.parser')

    editais_encontrados = []

    # 3. A LÓGICA DE EXTRAÇÃO (O coração do scraper)
    # Exemplo genérico: Busca todos os links (tags <a>) dentro de artigos
    # Terá de ajustar o 'a' e a 'class_' conforme a estrutura real do site alvo
    elementos_html = site.find_all('a', href=True)

    for elemento in elementos_html:
        titulo = elemento.text.strip()
        link = elemento.get('href')

        # Corrige links relativos (ex: "/grant-2026" vira "https://site.org/grant-2026")
        if link and link.startswith('/'):
            link = f"https://url-base-do-site.org{link}"

        editais_encontrados.append((id_sociedade, titulo, link, categoria))
        print(f"Detectado: {titulo}")

    return editais_encontrados

if __name__ == "__main__":

    # URL atualizada de fundos e prêmios do IEEE
    url_teste = "https://students.ieee.org/membership-benefits/ieee-benefits/funds-and-awards/"

    # ID representativo para o Comitê Estudantil
    id_sociedade_sac = 46

    print("Iniciando o motor de busca...")
    editais = buscar_editais_reais(url_teste, id_sociedade_sac, "Financiamento Estudantil")

    print(f"\nTotal de links encontrados: {len(editais)}")