from app.Models.User import User
from app.DataBaseModule import DataBase


database = DataBase()

def getUser(hash):

    values = database.Select(f"""SELECT * FROM doc.tb_user WHERE "AuthHash" = '{hash}'""")

    if len(values) <= 0:
        return None
    
    value = values[0]
        

    user:User = User('','')
    user.id = value['IdUser']
    user.login = value['Login']
    user.nome = value['Nome']
    user.funcao = value['IdFuncao']
    user.hash = value['AuthHash']

    return vars(user)


def postUser(user:User):
    error = database.Execute("""
        insert into doc.tb_user
        ("Nome","IdFuncao","AuthHash","Login")
        VALUES
        ('{}',{},'{}','{}')
    """.format(user.nome, user.funcao, user.hash, user.login))

    errorMessage = 'Criado com Sucesso',200

    if not error[0] and str(error[1]) == "UniqueViolation":
        errorMessage = 'Usuario Já Existe',500

    return errorMessage


def putUser(user:User):
    error = database.Execute("""
        UPDATE doc.tb_user
        SET
        "Nome" = '{}'
        ,"IdFuncao" = {}
        ,"AuthHash" = '{}'
        ,"Login" = '{}'
                             
        WHERE "Login" = '{}'
    """.format(user.nome, user.funcao, user.hash, user.login, user.login))

    errorMessage = 'Atualizado com Sucesso',200

    return errorMessage



def deleteUser(user:User):
    error = database.Execute("""
        DELETE FROM doc.tb_user  
        WHERE "Login" = '{}'
    """.format(user.login))

    errorMessage = 'Deletado com Sucesso',200

    return errorMessage
