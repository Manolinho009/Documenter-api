

class Documentation:

    titulo:str
    descricao:str = None
    abas:list = None
    imagemCapa:str = None
    commitText:str = None
    versao:str = None
    status:int = None
    dataAlteracao:str = None
    usuarioAlteracao:int = None
    tags:list = None

    def __init__(self, titulo) :
        
        self.titulo = titulo
        
        pass