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

if __name__ == "__main__":
    testar_conexao()