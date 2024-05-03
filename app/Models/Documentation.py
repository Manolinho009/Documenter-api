from app.Models.User import User

class Documentation:

    titulo:str
    descricao:str = None
    abas:list = None
    imagemCapa:str = None
    commitText:str = None
    versao:str = None
    status:int = None
    dataAlteracao:str = None
    usuarioAlteracao:User = None
    tags:list = None
    id:int 

    def __init__(self, titulo) :
        
        self.titulo = titulo
        
        pass