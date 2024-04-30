import json

from app import application
from app.DAOs import UserDAO,DocumentationDAO
from app.Services import LoginService
from app.Models.User import User
from app.Models.Documentation import Documentation

from functools import wraps

from flask import make_response,request, abort, redirect


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if not 'Authorization' in request.headers:
               abort(401)

            valid = None
            data = request.headers['Authorization'].encode('ascii','ignore')
            token = str.replace(str(data), 'Bearer ','')
            try:
                valid = LoginService.validateHash(hash=token)
            except:
                
                
                abort(401)

            return f(valid, *args, **kws)            
    return decorated_function


#############################################################################


@application.route('/')
@authorize
def index(valid):
    print(valid)
    a = request.cookies.get(key='user')
    hash = LoginService.generateHash('thithi','123')
    value = UserDAO.getUser(hash)

    return make_response(a)

@application.route('/user/login', methods=['POST'])
def userLogin():
    response = {}
    if request.is_json:
        values = request.get_json()

        hash = LoginService.generateHash(values['login'],values['password'])
        value = UserDAO.getUser(hash)

        
        if value is not None:
            user = json.dumps(value)
            token = 'Bearer '+LoginService.createValidateHash(hash)

            res = make_response({"user":json.loads(user), "token":token},200)
            res.set_cookie('user', value=user)
            res.headers['Authorization'] = token
            
            return res
        else:
            return {'status':'Usuario ou senha não existem'},500
        

    return {}

@application.route('/user/create', methods=['POST'])
# @authorize
def userCreate():
    response={}
    if request.is_json:
        values = request.get_json()
        
        user = User(values['login'],values['password'])
        user.nome = values['nome']
        user.funcao = values['funcao']

        createdUser = UserDAO.postUser(user)

        response['status'] = createdUser[0]
        code = createdUser[1]

        return make_response(response,code)

    
    return {}


@application.route('/user/update', methods=['PUT'])
@authorize
def userUpdate(a):
    response = {}
    if request.is_json:
        values = request.get_json()
        
        user = User(values['login'],values['password'])
        user.nome = values['nome']
        user.funcao = values['funcao']

        updatedUser = UserDAO.putUser(user)

        response['status'] = updatedUser[0]
        code = updatedUser[1]


        return make_response(response,code)
    
    return {}




@application.route('/user/delete', methods=['DELETE'])
@authorize
def userDelete(a):
    response = {}
    if request.is_json:
        values = request.get_json()
        
        user = User(values['login'],values['password'])
        user.nome = values['nome']
        user.funcao = values['funcao']

        deletedUser = UserDAO.deleteUser(user)
        response['status'] = deletedUser[0]
        code = deletedUser[1]


        return make_response(response,code)
    
    return {}


############################################################################



@application.route('/documentation/user/all', methods=['POST'])
@authorize
def getAllUserDocumentation(valid):
    cookie = request.get_json()['user']

    user = json.loads(cookie)
    objUser = User(
        login=user['login'],
        password=''
    )
    objUser.id = user['id']
    objUser.hash = user['hash']
    objUser.nome = user['nome']
    objUser.funcao = user['funcao']


    documentation = DocumentationDAO.getDocumentationAllUser(objUser)

    if documentation is None:
        return 'Não Existe'
    
    return make_response(documentation)

#####################################################################


@application.route('/documentation/<id>')
@authorize
def getDocumentation(valid, id):
    a = request.cookies.get(key='user')

    documentation = DocumentationDAO.getDocumentation(id)

    if documentation is None:
        return {'status':'Não Existe'},500
    
    return make_response(documentation)



@application.route('/documentation/create', methods=['POST'])
@authorize
def createDocumentation(valid):
    a = request.cookies.get(key='user')
    # {
    #     "tags":[]
    #     ,"titulo":"123"
    #     ,"sections":[]
    #     ,"commitText":""
    #     ,"sectionsChanges":[]
    #     ,"version":""
    #     ,"status":""
    #     ,"dh_alteracao":""
    #     ,"user_alteracao":{"login":"thithi","nome":"Thiago Rocha"}
    #     ,"descricao":"123"
    # }
    response = {}
    if request.is_json:
        values = request.get_json()

        documentation = Documentation(titulo=values['titulo'])

        documentation.descricao = values['descricao']
        documentation.abas = values['sections']
        documentation.imagemCapa = values['imagemCapa']
        documentation.commitText = values['commitText']
        documentation.versao = values['version']
        documentation.status = values['status']
        documentation.dataAlteracao = values['dh_alteracao']
        documentation.usuarioAlteracao = values['idUser']
        documentation.tags = values['tags']

        doc = DocumentationDAO.postDocumentation(documentation)
        response['status'] = doc[0]
        code = doc[1]



    if doc is None:
        response['status'] = 'Não Existe'
        code = 500
    
    return make_response(response,code)

@application.route('/documentation/update', methods=['PUT'])
@authorize
def updateDocumentation(valid):
    a = request.cookies.get(key='user')
    response = {}

    if request.is_json:
        values = request.get_json()

        documentation = Documentation(titulo=values['titulo'])

        documentation.descricao = values['descricao']
        documentation.abas = values['sections']
        documentation.imagemCapa = values['imagemCapa']
        documentation.commitText = values['commitText']
        documentation.versao = values['version']
        documentation.status = values['status']
        documentation.dataAlteracao = values['dh_alteracao']
        documentation.usuarioAlteracao = values['user_alteracao']
        documentation.tags = values['tags']

        doc = DocumentationDAO.putDocumentation(documentation)
        response["status"] = doc[0]
        code = doc[1]

    if doc is None:
        response["status"] = 'Não Existe'
        code = 500
    
    return make_response(response,code)



@application.route('/documentation/delete', methods=['DELETE'])
@authorize
def deleteDocumentation(valid):
    a = request.cookies.get(key='user')
    response = {}
 
    if request.is_json:
        values = request.get_json()

        documentation = Documentation(titulo=values['titulo'])

        doc = DocumentationDAO.deleteDocumentation(documentation)
        response['status'] = doc[0]
        code = doc[1]
    if doc is None:
        
        response['status'] = 'Não Existe'
        code = 500
    
    return make_response(response,code)








