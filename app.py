from flask import Flask, jsonify, request

from BBDD.conecctor import BBDD

from models.user import User

app = Flask(__name__)

connector = BBDD() # Conexión a la BBDD de MongoDB



#Funcion para no tener estar formateando el json todo el rato
def ret(result, status = 200, error = ""):
    return jsonify({
        "result": result,
        "status": status,
        "error": error
    })



@app.route('/')
def origin():
    return ret("Bienvenido a FULL")


@app.route('/api')
def api():
    return ret("Bienvenido a la API de FULL")


@app.route('/api/ping')
def ping():
    try:
        result = connector.ping()
        return ret(result)
    except Exception as e:
        return ret("Error al hacer ping", 500, str(e))


@app.route('/api/users')
def getUsers():
    try:
        result = connector.client.FULL.users.find()
    
        listResult = []

        for documento in result:
            documento['_id'] = str(documento['_id']) 
            listResult.append(documento)

        if len(listResult) > 0:
            return ret(listResult)
        else:
            return ret("No hay usuarios registrados", 404)
        
    except Exception as e:
        return ret("Error al obtener los usuarios", 500, str(e))


@app.route('/api/users/<string:username>')
def getUserByName(username):
    try:
        result = connector.client.FULL.users.find_one({ "username": username})

        if result:
            result['_id'] = str(result['_id'])  # Convertir el ObjectId en un string
            return ret(result)
        else:
            return ret("No existe el usuario "+username, 404)
        
    except Exception as e:
        return ret("Error al obtener el usuario "+username, 500, str(e))


@app.route('/api/users/email/<string:username>', methods=['PUT'])
def updateEmail(username):
    email = request.json['email']

    try:
        connector.client.FULL.users.update_one({"username": username}, {"$set": {"email": email}})

        return ret("Email del usuario "+username+" actualizado correctamente")
    
    except Exception as e:
        return ret("Error al actualizar el email del usuario "+username, 500, str(e))


@app.route('/api/users/phone/<string:username>', methods=['PUT'])
def updatePhone(username):
    phone = request.json['phone']

    try:
        connector.client.FULL.users.update_one({"username": username}, {"$set": {"phone": phone}})

        return ret("Teléfono del usuario "+username+" actualizado correctamente")
    
    except Exception as e:
        return ret("Error al actualizar el teléfono del usuario "+username, 500, str(e))


@app.route('/api/users/<string:username>', methods=['DELETE'])
def deleteUser(username):
    try:
        connector.client.FULL.users.delete_one({"username": username})

        return ret("Usuario "+username+" eliminado correctamente")
    
    except Exception as e:
        return ret("Error al eliminar el usuario "+username, 500, str(e))


@app.route('/api/users/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    try:
        result = User.login(username, password, connector)

        if result:
            result['_id'] = str(result['_id'])
            return ret(True)
        else:
            return ret(False, 401)
        
    except Exception as e:
        return ret("Error al hacer login", 500, str(e))
    

@app.route('/api/users/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    phone = request.json['phone']
    admin = request.json['admin']
    status = request.json['status']

    try:
        user = User(username, password, email, phone, admin, status, connector)
        user.register()

        return ret("Usuario "+username+" registrado correctamente")
        
    except Exception as e:
        return ret("Error al registrar el usuario "+username, 500, str(e))


if __name__ == '__main__':
    app.run()