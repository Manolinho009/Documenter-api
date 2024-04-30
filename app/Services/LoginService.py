import hashlib 
import datetime
import base64
from app import application


SECRET_KEY = application.config['SECRET_KEY']

def encodeB64(value):

    value = value.encode("ascii")
    string_bytes = value

    base64_bytes = base64.b64encode(string_bytes) 
    base64_string = base64_bytes.decode("ascii") 
    
    return base64_string



def decodeB64(hash):
    base64_string = str(hash).replace("b'",'').replace("'",'').strip()
    base64_bytes = base64_string.encode("ascii") 

    string_bytes = base64.b64decode(base64_bytes) 
    decoded_value = string_bytes.decode("ascii") 

    return decoded_value
    



## Função para gerar uma HASH de authenticação baseada em uma chave secreta
def generateHash(login, password):

    # Criando o SHA-256 hash object
    sha256_hash = hashlib.sha256()
    value = f"{SECRET_KEY}{login}{password}".encode("utf-8")
    sha256_hash.update(bytes(value))
    hash_hex = sha256_hash.hexdigest()
  
    return hash_hex


## Valida a Hash enviada comparando com a Hash gerada a partir de um login e senha
def createValidateHash(hash):
    secretHash = encodeB64(SECRET_KEY)
    userHash = encodeB64(f"{hash},valid")
    hashToken = encodeB64(f"{userHash}{secretHash}")
    return hashToken

## Valida a Hash enviada comparando com a Hash gerada a partir de um login e senha
def validateHash(hash):
    secretHash = encodeB64(SECRET_KEY)

    decoded_value = decodeB64(hash=f"{hash}")
    decoded_value = decodeB64(decoded_value.replace(secretHash,""))

    validates = decoded_value.split(',')

    if len(validates) >= 0 :
        return validates[1] == "valid"
    else:
        return False