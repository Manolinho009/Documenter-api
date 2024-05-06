from app.Models.Tag import Tag
from app.DataBaseModule import DataBase


database = DataBase()

def postTag(tag:Tag):

    error = database.Execute("""
        insert into doc.tb_tag
        ("NomeTag","CorTag")
        VALUES
        ('{}','{}')
    """.format(tag.nome, tag.cor))

    errorMessage = 'Criado com Sucesso',200

    if not error[0] and str(error[1]) == "UniqueViolation":
        errorMessage = 'Tag Já Existe',500

    return errorMessage