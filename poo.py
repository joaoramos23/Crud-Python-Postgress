#POO + BD

import psycopg2
import os 
from dotenv import load_dotenv

def limpar_console():
    os.system('cls')

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        self.cursor = self.connection.cursor()
        self.create_table()
    
    def create_table(self):
        create_table_query = """CREATE TABLE IF NOT EXISTS funcionarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255),
            funcao VARCHAR(255),
            salario DECIMAL
        )"""
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def insert_funcionario(self,nome,funcao,salario):
        insert_query = """INSERT INTO funcionarios (nome,funcao,salario) VALUES (%s,%s,%s) RETURNING id"""
        self.cursor.execute(insert_query, (nome, funcao, salario))
        self.connection.commit()
        return self.cursor.fetchone()[0]
    
    def update_funcionario(self,id,funcao,salario):
        update_query = """UPDATE funcionarios SET funcao = %s, salario = %s WHERE id = %s RETURNING *"""
        self.cursor.execute(update_query, (funcao,float(salario),int(id)))
        self.connection.commit()
        print(f"Linha atualizada: {self.cursor.fetchone()[0]}")

    def delete_funcionario(self,id):
        delete_query = """DELETE FROM funcionarios WHERE id = %s RETURNING *"""
        self.cursor.execute(delete_query, id)
        self.connection.commit()
        print(f"Linha deletada: {self.cursor.fetchone()[0]}")
    
    def close(self):
        self.cursor.close()
        self.connection.close()


class Funcionario:
    def __init__(self, db, nome, funcao, salario):
        self.nome = nome
        self.funcao = funcao
        self.salario = salario
        self.salvar_no_banco(db)

    def salvar_no_banco(self, db):
        funcionario_id = db.insert_funcionario(self.nome,self.funcao,self.salario)
        print(f"Funcionário {self.nome} inserido com sucesso com ID {funcionario_id}.")

if __name__ == "__main__":
    db = Database()

    while True:
        opcaoInterface = input('1 - Criar Funcionario\n2 - Editar Post\n3 - Deletar Post\n4 - Fechar Interface\nEscolha uma opção:')
        limpar_console()
        match opcaoInterface:
            case '1':
                nome = input("Digite o nome do funcionario: ")
                funcao = input(f"Digite a função do funcionario {nome}: ")
                salario = float(input(f"Digite o salario do funcionario {nome}: "))
                funcionario = Funcionario(db,nome,funcao,salario)
            case '2':
                id_funcionario = input("\nDigite o ID para ATUALIZAR:")
                funcao = input(f"Digite a função para atualizar: ")
                salario = float(input(f"Digite o salario para atualizar: "))
                db.update_funcionario(id_funcionario,funcao,salario)
            case '3':
                id_funcionario = input("\nDigite o ID para Deletar:")
                db.delete_funcionario(id_funcionario)
            case '4':
                break
            case _:
                print("Escolha uma opção valida!")    
    db.close()
