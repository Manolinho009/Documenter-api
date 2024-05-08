import json

from app import application
from app.DAOs import UserDAO,DocumentationDAO,TagDAO
from app.Services import LoginService
from app.Models.User import User
from app.Models.Documentation import Documentation
from app.Models.Tag import Tag

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
    # print(valid)
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
            imagem = str(value['imagem'])
            # del value['imagem']

            user = json.dumps(value)
            token = 'Bearer '+LoginService.createValidateHash(hash)

            resposta = {"user":json.loads(user), "token":token, "imagem":imagem}

            res = make_response(resposta,200)
            # res.set_cookie('user', value=user)
            # res.set_cookie('imagemPerfil', value=imagem)
            
            res.headers['Authorization'] = token
            
            return res
        else:
            return {'status':'Usuario ou senha não existem'},500
        

    return {}



@application.route('/user/all', methods=['GET'])
def userAll():
    retorno  = UserDAO.getAll()
    # print(retorno)
    if retorno is None:
        return make_response({'status':'Erro na consulta'},500) 

    return make_response(retorno)


@application.route('/user/image', methods=['POST'])
def userImageChange():
    response = {}
    if request.is_json:
        values = request.get_json()

        user = User(values['login'],'')
        user.id = values['id']
        user.nome = values['nome']
        user.funcao = values['funcao']
        user.imagem = values['imagem']

        retorno  = UserDAO.changeUserImage(user)
        
        response['status'] = retorno[0]
        code = retorno[1]
        
        return make_response(response,code)
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


@application.route('/tag/create', methods=['POST'])
# @authorize
def createTag():
    response = {}
    code = 200
    if request.is_json:
        values = request.get_json()
        # print(values)
        tag = Tag(
            values['textoTag'],
            values['corTag']
        )

        retorno = TagDAO.postTag(tag)

        response['status'] = retorno[0]
        code = retorno[1]

        if retorno is None:
            response['status'] = 'Não Existe'
            code = 500
            
    return make_response(response, code)

############################################################################

@application.route('/documentation/tags/all', methods=['GET'])
def getTagsPadrao():

    result = DocumentationDAO.selectTags()

    if result is None:
        return make_response([])
    return make_response(result)


@application.route('/documentation/user/all', methods=['POST'])
@authorize
def getAllUserDocumentation(valid):
    value = request.get_json()
    user = value
    objUser = User(
        login=user['login'],
        password=''
    )
    objUser.id = user['id']
    objUser.hash = user['hash']
    objUser.nome = user['nome']
    objUser.funcao = user['funcao']
    objUser.projetos = user['projetos']


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
        # print(values)
        documentation.descricao = values['descricao']
        documentation.abas = values['abas']
        documentation.imagemCapa = values['imagemCapa']
        documentation.commitText = values['commitText']
        documentation.versao = values['versao']
        documentation.status = values['status']
        documentation.dataAlteracao = values['dataAlteracao']
        documentation.usuarioAlteracao = values['usuarioAlteracao']
        documentation.tags = values['tags']

        doc = DocumentationDAO.postDocumentation(documentation)
        response['status'] = doc[0]
        code = doc[1]



    if doc is None:
        response['status'] = 'Não Existe'
        code = 500
    
    return make_response(response,code)



@application.route('/documentation/user/dell', methods=['POST'])
@authorize
def dellUserDocumentation(valid):
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

        # print(values)
        
        documentation = Documentation(titulo=values['documentation']['titulo'])
        documentation.id = values['documentation']['id']

        doc = DocumentationDAO.deleteUserDocumentation(documentation,values['idUser'])
        
        response["status"] = doc[0]
        code = doc[1]

    if doc is None:
        response["status"] = 'Não Existe'
        code = 500
    
    return make_response(response,code)

@application.route('/documentation/user/add', methods=['POST'])
@authorize
def addUserDocumentation(valid):
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

        # print(values)

        documentation = Documentation(titulo=values['documentation']['titulo'])
        documentation.id = values['documentation']['id']

        doc = DocumentationDAO.postUserDocumentation(documentation,values['idUser'])
        
        response["status"] = doc[0]
        code = doc[1]

    if doc is None:
        response["status"] = 'Não Existe'
        code = 500
    
    return make_response(response,code)



@application.route('/documentation/users', methods=['POST'])
@authorize
def usersDocumentation(valid):
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

        # print(values)
        documentation.descricao = values['descricao']
        documentation.abas = values['abas']
        documentation.imagemCapa = values['imagemCapa']
        documentation.commitText = values['commitText']
        documentation.versao = values['versao']
        documentation.status = values['status']
        documentation.dataAlteracao = values['dataAlteracao']
        documentation.usuarioAlteracao = values['usuarioAlteracao']
        documentation.id = values['id']
        documentation.tags = values['tags']

        doc = DocumentationDAO.getUsersDocumentation(documentation)
        code = 200 #doc[1]

    if doc is None:
        response['status'] = 'Não Existe'
        code = 500
    
    return make_response(doc,code)

@application.route('/documentation/update', methods=['PUT'])
@authorize
def updateDocumentation(valid):
    a = request.cookies.get(key='user')
    response = {}

    if request.is_json:
        values = request.get_json()
        
        documentation = Documentation(titulo=values['titulo'])

        documentation.descricao = values['descricao']
        documentation.abas = values['abas']
        documentation.imagemCapa = values['imagemCapa']
        documentation.commitText = values['commitText']
        documentation.versao = values['versao']
        documentation.status = values['status']
        documentation.dataAlteracao = values['dataAlteracao']
        documentation.usuarioAlteracao = values['usuarioAlteracao']
        documentation.tags = values['tags']

        doc = DocumentationDAO.putDocumentation(documentation)
        response["status"] = doc[0]
        code = doc[1]

    if doc is None:
        response["status"] = 'Não Existe'
        code = 500
    
    return make_response(response,code)



@application.route('/documentation/delete/<titulo>', methods=['DELETE'])
# @authorize
def deleteDocumentation(titulo):
    # print(titulo)
    a = request.cookies.get(key='user')

    response = {}
 
    documentation = Documentation(titulo=titulo)

    doc = DocumentationDAO.deleteDocumentation(documentation)
    response['status'] = doc[0]
    code = doc[1]

    if doc is None:
        
        response['status'] = 'Não Existe'
        code = 500

    return make_response(response,code)









