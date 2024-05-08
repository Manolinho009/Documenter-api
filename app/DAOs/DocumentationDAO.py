from app.DataBaseModule import DataBase
from app.Models.Documentation import Documentation
from app.Models.User import User

import json

database = DataBase()

def getDocumentationAllUser(user:User):

    # if ':' in user.projetos:
    #     user.projetos.remove(':')
    #     if len(user.projetos)<=0:
    #         user.projetos.append('0:0')

    values = database.Select(f"""
                            SELECT 
                                doc."Titulo"
                                , doc."Descricao"
                                , doc."Abas"
                                , doc."ImagemCapa"
                                , doc."CommitText"
                                , doc."Versao"
                                , doc."Status"
                                , doc."DataAlteracao"::character varying
                                , doc."UsuarioAlteracao"
                                , tbu."Nome" as "NomeUsuarioAlteracao"
                                , doc."IdDocumentacao"
	                            ,CONCAT('[',STRING_AGG(CONCAT('{'{'}"NomeTag":"',tags."NomeTag",'","CorTag":"',tags."CorTag",'","IdTag":"',tags."IdTag",'"{'}'}')::character varying,','),']') as "Tags"
                            FROM doc.tb_documentation doc
                            LEFT JOIN  DOC.TB_TAG tags
                            ON tags."IdTag"::character varying = any(doc."Tags")
                            LEFT JOIN  DOC.TB_USER tbu
                            ON tbu."IdUser" = doc."UsuarioAlteracao"
                             
                            WHERE (doc."IdDocumentacao" in (SELECT "IdDocumentacao" FROM DOC.TB_DOCUMENTATION_USER WHERE "IdUser" =  {user.id}))
                                AND doc."Status" = 1

                            GROUP BY doc."Titulo"
                                , doc."Descricao"
                                , doc."ImagemCapa"
                                , doc."CommitText"
                                , doc."Versao"
                                , doc."Status"
                                , doc."DataAlteracao"
                                , doc."UsuarioAlteracao"
                                , tbu."Nome"
                                , doc."IdDocumentacao"
                            
                              """)

    print(user.id)
    if values and len(values) <= 0:
        return None
    
    result = []
    for value in values:
        userAlteracao = User('','')
        userAlteracao.id = value['UsuarioAlteracao']
        userAlteracao.nome = value['NomeUsuarioAlteracao']
        
        documentation:Documentation = Documentation(value['Titulo'])
        documentation.descricao = value['Descricao']
        documentation.abas = value['Abas']
        documentation.imagemCapa = value['ImagemCapa']
        documentation.commitText = value['CommitText']
        documentation.versao = value['Versao']
        documentation.status = value['Status']
        documentation.dataAlteracao = value['DataAlteracao']
        documentation.usuarioAlteracao = vars(userAlteracao)

        documentation.tags = json.loads(value['Tags'])

        documentation.id = value['IdDocumentacao']

        result.append(vars(documentation))
   
    return result


def getUsersDocumentation(documentation:Documentation):

    
    values = database.Select(f"""
                                SELECT tbu."IdUser"
                                        ,"Nome"
                                        ,"AuthHash"
                                        ,"Login"
                                        ,TBF."NomeFuncao" 
                                FROM DOC.TB_USER TBU
                                LEFT JOIN DOC.TB_DOCUMENTATION_USER TBDU
                                ON TBDU."IdUser" = TBU."IdUser"
                                LEFT JOIN DOC.TB_FUNCAO TBF
                                ON TBF."IdFuncao" = TBU."IdFuncao"
                                WHERE (TBDU."IdDocumentacao" = {documentation.id} or TBU."IdUser" = {documentation.usuarioAlteracao['id']}) """)

    if len(values) <= 0:
        return None
    
    result = []
    for value in values:
        user = User(
                login='',
                password=''
            )
        user.nome = value['Nome']
        user.id = value['IdUser']
        user.funcao = value['NomeFuncao']

        result.append(
           vars(user)
        )
        

    return result


def getDocumentation(IdDocumentation):

    
    values = database.Select(f"""SELECT * FROM doc.tb_documentation WHERE "IdDocumentacao" = {IdDocumentation} """)

    if len(values) <= 0:
        return None
    
    value = values[0]
    
    
    documentation:Documentation = Documentation(value['Titulo'])
    documentation.descricao = value['Descricao']
    documentation.abas = value['Abas']
    documentation.imagemCapa = value['ImagemCapa']
    documentation.commitText = value['CommitText']
    documentation.versao = value['Versao']
    documentation.status = value['Status']
    documentation.dataAlteracao = value['DataAlteracao']
    documentation.usuarioAlteracao = value['UsuarioAlteracao']
    documentation.tags = value['Tags']
    documentation.id = value['id']
   
    return vars(documentation)


def postDocumentation(documentation:Documentation):
    error = database.Execute("""
        INSERT INTO doc.tb_documentation(
        "Titulo", "Descricao", "Abas", "ImagemCapa", "CommitText", "Versao", "Status", "DataAlteracao", "UsuarioAlteracao", "Tags")
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}', array{}::character varying[]);
    """.format(documentation.titulo
                , documentation.descricao
                , documentation.abas
                , documentation.imagemCapa
                , documentation.commitText
                , documentation.versao
                , documentation.status
                , documentation.dataAlteracao
                , documentation.usuarioAlteracao['id']
                , str(documentation.tags)
                ))
    
    error = database.Execute("""
        INSERT INTO DOC.TB_DOCUMENTATION_USER
        VALUES ((SELECT "IdDocumentacao" FROM doc.tb_documentation WHERE "Titulo" = '{}' LIMIT 1),{},1);
    """.format(documentation.titulo
                , documentation.usuarioAlteracao['id']
                ))

    errorMessage = 'Criado com Sucesso',200

    if error is None:
        return 'Erro inesperado',500


    if not error[0] and str(error[1]) == "UniqueViolation":
        errorMessage = 'Documentação Já existe com esse titulo',500

    return errorMessage


def postUserDocumentation(documentation:Documentation,userId):
    error = database.Execute("""
        INSERT INTO DOC.TB_DOCUMENTATION_USER
        VALUES ({},{},3)
    """.format(documentation.id
                , userId
                ))

    errorMessage = 'Criado com Sucesso',200

    if error is None:
        return 'Erro inesperado',500


    if not error[0] and str(error[1]) == "UniqueViolation":
        errorMessage = 'Esse usuario já foi adicionado',500

    return errorMessage
    

def putDocumentation(documentation:Documentation):

    error = database.Execute("""
        UPDATE doc.tb_documentation
        SET
            "Descricao" =  '{}'
            , "Abas" =  '{}'
            , "ImagemCapa" =  '{}'
            , "CommitText" =  '{}'
            , "Versao" =  '{}'
            , "Status" =  {}
            , "DataAlteracao" =  '{}'
            , "UsuarioAlteracao" =  '{}'
            , "Tags" = array{}::character varying[]
                             
        WHERE "Titulo" =  '{}'
    """.format(documentation.descricao
                , json.dumps(documentation.abas)
                , documentation.imagemCapa
                , documentation.commitText
                , documentation.versao
                , documentation.status
                , documentation.dataAlteracao
                , documentation.usuarioAlteracao['id']
                , str(documentation.tags)
                , documentation.titulo
                ))

    errorMessage = 'Atualizado com Sucesso',200

    if error is None:
        return 'Erro inesperado',500


    if not error[0] and str(error[1]) == "UniqueViolation":
        errorMessage = 'Documentação Já existe com esse titulo',500

    return errorMessage


def deleteUserDocumentation(documentation:Documentation,userId):
    error = database.Execute("""
        DELETE FROM DOC.TB_DOCUMENTATION_USER
        WHERE "IdDocumentacao" = {} and "IdUser" = {}
    """.format(documentation.id
                , userId
                ))

    errorMessage = 'Deletado com Sucesso',200

    if error is None:
        return 'Erro inesperado',500


    if not error[0] and str(error[1]) == "UniqueViolation":
        errorMessage = 'Esse usuario já foi Apagado',500

    return errorMessage
    

def putDocumentation(documentation:Documentation):

    error = database.Execute("""
        UPDATE doc.tb_documentation
        SET
            "Descricao" =  '{}'
            , "Abas" =  '{}'
            , "ImagemCapa" =  '{}'
            , "CommitText" =  '{}'
            , "Versao" =  '{}'
            , "Status" =  {}
            , "DataAlteracao" =  '{}'
            , "UsuarioAlteracao" =  '{}'
            , "Tags" = array{}::character varying[]
                             
        WHERE "Titulo" =  '{}'
    """.format(documentation.descricao
                , json.dumps(documentation.abas)
                , documentation.imagemCapa
                , documentation.commitText
                , documentation.versao
                , documentation.status
                , documentation.dataAlteracao
                , documentation.usuarioAlteracao['id']
                , str(documentation.tags)
                , documentation.titulo
                ))

    errorMessage = 'Atualizado com Sucesso',200

    if error is None:
        return 'Erro inesperado',500


    if not error[0] and str(error[1]) == "UniqueViolation":
        errorMessage = 'Documentação Já existe com esse titulo',500

    return errorMessage


def deleteDocumentation(documentation:Documentation):
    error = database.Execute("""
        
        WITH DOC AS (
        SELECT "IdDocumentacao" FROM doc.tb_documentation
        WHERE "Titulo" = '{}'	
        )
        DELETE FROM doc.tb_documentation_user
        WHERE "IdDocumentacao" in (SELECT "IdDocumentacao" FROM DOC);

        DELETE FROM doc.tb_documentation
        WHERE "Titulo" = '{}'                  
        
    """.format(documentation.titulo,documentation.titulo))

    errorMessage = 'Deletado com Sucesso',200

    if error is None:
        return 'Erro inesperado',500


    if not error[0] and str(error[1]) == "UniqueViolation":
        errorMessage = 'Documentação Já existe com esse titulo',500

    return errorMessage








def selectTags():
    values = database.Select("""
        SELECT * FROM DOC.TB_TAG
    """)

    if values and len(values) <= 0:
        return None
    
    result = []
    for value in values:
        result.append(value)

    return result