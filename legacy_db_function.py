import psycopg2

# CONEXÃO BANCO DE DADOS:
# PRECISA ALTERAR AS CREDENCIAIS DO SEU BANCO.

def dbConection():
    conn = psycopg2.connect(
        database="postgres",
        host="localhost",
        user="postgres",
        password="klo5s871",
        port="5432"
    )

    cursor = conn.cursor()
    return conn, cursor

# FUNÇÃO QUE CRIA TABELA CASO ELA NÃO EXISTA, E ADICIONA UM ID COMO SERIAL NA CRIAÇÃO DA TABELA. ELA IRÁ CRIAR TODAS AS COLUNAS COMO TEXT

def dbCreateTable(nameTable, columnsTable):

    conn, cursor = dbConection()

    dbColumns = "id serial primary key, "

    dbColumns = dbColumns + ", ".join([f"{coluna} TEXT" for coluna in columnsTable])

    cursor.execute("""CREATE TABLE IF NOT EXISTS public.{} ({});""".format(nameTable,dbColumns))

    conn.commit()
    cursor.close()
    conn.close()

