import app.Services.LoginService as loginService


class User:

    id:int

    nome:str
    funcao:str
    imagem:str
    
    projetos:list

    login:str
    password:str 

    hash:str

    ## Inicia o Objeto com um login e senha 
    def __init__(self, login, password) -> None:

        self.login = login
        self.password = password
        self.hash = loginService.generateHash(login=login, password=password)