from app.Models.User import User
from app.DataBaseModule import DataBase


database = DataBase()

def getAll():
    values = database.Select(f"""
                             SELECT 
                                tbu."IdUser"
                                ,"Nome"
                                ,"Login"
                                ,"NomeFuncao" 
                                ,COALESCE("Imagem",'../../../assets/imagemLogin.jpg') as "Imagem"
                            FROM DOC.TB_USER tbu
                            LEFT JOIN DOC.TB_FUNCAO tbf
                            ON tbu."IdFuncao" = tbf."IdFuncao"
                            LEFT JOIN DOC.TB_IMAGEM_USER tbiu
                            ON tbiu."IdUser" = tbu."IdUser"
                            
                            GROUP BY tbu."IdUser"
                                ,"Nome"
                                ,"Login"
                                ,"NomeFuncao" 
                                ,COALESCE("Imagem",'../../../assets/imagemLogin.jpg')                           
                             """)

    if len(values) <= 0:
        return None
    
    result = []
    for value in values:
        user:User = User('','')
        user.id = value['IdUser']
        user.login = value['Login']
        user.nome = value['Nome']
        user.funcao = value['NomeFuncao']
        user.imagem = value['Imagem']

        result.append(vars(user))

    return result

def getUser(hash):

    values = database.Select(f"""
                             SELECT 
                                tbu."IdUser"
                                ,"Nome"
                                ,"AuthHash"
                                ,"Login"
                                ,"NomeFuncao" 
                                ,COALESCE("Imagem",'../../../assets/imagemLogin.jpg') as "Imagem"
	                            ,COALESCE(STRING_AGG(CONCAT(tbdu."IdDocumentacao"::character varying,':',tbdu."IdAcesso"),','),'0') as "IdDocumentacoes"
                            FROM DOC.TB_USER tbu
                            LEFT JOIN DOC.TB_FUNCAO tbf
                            ON tbu."IdFuncao" = tbf."IdFuncao"
                            LEFT JOIN DOC.TB_IMAGEM_USER tbiu
                            ON tbiu."IdUser" = tbu."IdUser"
                            LEFT JOIN DOC.tb_documentation_user tbdu
                            ON tbdu."IdUser" = tbu."IdUser"
                            WHERE "AuthHash" = '{hash}'
                            GROUP BY tbu."IdUser"
                                ,"Nome"
                                ,"AuthHash"
                                ,"Login"
                                ,"NomeFuncao" 
                                ,COALESCE("Imagem",'../../../assets/imagemLogin.jpg')                           
                             """)

    if len(values) <= 0:
        return None
    
    value = values[0]
        

    user:User = User('','')
    user.id = value['IdUser']
    user.login = value['Login']
    user.nome = value['Nome']
    user.funcao = value['NomeFuncao']
    user.imagem = value['Imagem']
    user.hash = value['AuthHash']
    user.projetos = value['IdDocumentacoes'].split(',')

    return vars(user)


def postUser(user:User):
    error = database.Execute("""
        insert into doc.tb_user
        ("Nome","IdFuncao","AuthHash","Login")
        VALUES
        ('{}',{},'{}','{}')
    """.format(user.nome, user.funcao, user.hash, user.login))

    errorMessage = 'Criado com Sucesso',200
    print(error)
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

########################################


def changeUserImage(user:User):
    error = database.Execute("""
        INSERT INTO doc.tb_imagem_user ("IdUser", "Imagem")
        VALUES ({}, '{}')
        ON CONFLICT ("IdUser") DO UPDATE
        SET "Imagem" = EXCLUDED."Imagem";
    """.format(user.id, user.imagem))

    errorMessage = 'Registrado com Sucesso',200

    return errorMessage