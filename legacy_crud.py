import legacy_db_function
from tabulate import tabulate
import os

# LIMPAR CONSOLE

def limpar_console():
    os.system('cls')


# VOCÊ PODE ADICIONAR QUANTAS COLUNAS VOCÊ ACHAR NECESSARIO. BASTA ANTES DE RODAR O CODIGO ADICIONAR AS COLUNAS. A QUANTIDADE DE COLUNAS É A QUANTIDADE DE INPUTS QUE A APLICAÇÃO IRÁ PEDIR, ESTÁ TUDO DINAMICO.

columnsTable = ["nome","salario","idade"] # COLUNAS DO BANCO DE DADOS
nameTable = "crud_empregado" # NOME DA TABELA PARA CRIAR E INSERIR OS DADOS

# CRIAR TABELA DE ACORDO COM O NOME DA TABELA E AS COLUNAS:

legacy_db_function.dbCreateTable(nameTable,columnsTable)


# CREATE
def dbCriarPost(dadosCriarPost,dbColumns):

    conn, cursor = legacy_db_function.dbConection()

    dadosCriarPostComAspas = ["'{}'".format(item) for item in dadosCriarPost]
    cursor.execute("""INSERT INTO public.{} ({}) VALUES ({});""".format(nameTable,", ".join(dbColumns),", ".join(dadosCriarPostComAspas)))
     
    conn.commit()
    cursor.close()
    conn.close()


# READ
def dbLerPosts(verificarId = None):
    conn, cursor = legacy_db_function.dbConection()

    if (verificarId):
        cursor.execute("""SELECT * FROM public.{} WHERE id = {};""".format(nameTable,verificarId))
    else:
        cursor.execute("""SELECT * FROM public.{};""".format(nameTable))

    nomesColunas = [desc[0] for desc in cursor.description]
    valoresDb = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return nomesColunas,valoresDb

# UPDATE
def dbUpdatePost(dadosAtualizarPosts,dbColumns,idAtualizar):
    
    conn, cursor = legacy_db_function.dbConection()

    dadosAtualizarPostComAspas = ["'{}'".format(item) for item in dadosAtualizarPosts]

    cursor.execute("""UPDATE public.{} SET {} WHERE id = {};""".format(nameTable,", ".join(f"{dbColumn} = {dadosAtualizarPostComAspa}" for dbColumn, dadosAtualizarPostComAspa in zip(dbColumns, dadosAtualizarPostComAspas)),int(idAtualizar)))
     
    conn.commit()
    cursor.close()
    conn.close()


# DELETE
def dbDeletePost(idDeletar):
    
    conn, cursor = legacy_db_function.dbConection()

    cursor.execute("""DELETE FROM public.{} WHERE id = {};""".format(nameTable,int(idDeletar)))
     
    conn.commit()
    cursor.close()
    conn.close()



def main():

    def percorrerInputs(labelsInputs):
        inputsValues = []
        for inputs in labelsInputs:
            inputsValues.append(input("Digite o {}:".format(inputs)))

        return inputsValues
    
    interfaceVerificar = True

    while interfaceVerificar:
        opcaoInterface = input('1 - Criar Post\n2 - Ler Posts\n3 - Editar Post\n4 - Deletar Post\n5 - Fechar Interface\nEscolha uma opção:')
        limpar_console()
        match opcaoInterface:
            case '1':
                dbCriarPost(percorrerInputs(columnsTable),columnsTable)
                limpar_console()
            case '2':
                dbLerPosts()
                sairLeitura = input("\n Aperte Enter para voltar ao menu.")
                limpar_console()
            case '3':
                dbLerPosts()
                idAtualizar = input("\nDigite o ID para ATUALIZAR:")
                dbUpdatePost(percorrerInputs(columnsTable),columnsTable,idAtualizar)
                limpar_console()
                print("Dados atualizados:")
                dbLerPosts(idAtualizar)
                sairLeitura = input("\n Aperte Enter para voltar ao menu.")
                limpar_console()
            case '4':
                dbLerPosts()
                idDeletar = input("\nDigite o ID para DELETAR:")
                limpar_console()
                dbDeletePost(idDeletar)
            case '5':
                interfaceVerificar = False




