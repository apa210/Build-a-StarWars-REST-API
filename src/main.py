"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Planeta, Favorito
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

##------------------------------------------------Usuarios
@app.route('/user', methods=['GET'])
def get_all_user():

    users = User.query.all() # esto obtiene todos los registros de la tabla User
    results = list(map(lambda item: item.serialize(), users)) #esto serializa los datos del arrays users

    return jsonify(results), 200

@app.route('/user/favorites', methods=['GET'])
def get_all_favorites_user():

    favoritos = Favorito.query.filter_by(user_id=1).all()
    results = list(map(lambda item: item.serialize(), favoritos))

    return jsonify(results), 200

@app.route('/user/create', methods=['POST'])
def create_user():
    body = json.loads(request.data)

    query_user = User.query.filter_by(email=body["email"]).first()
    
    if query_user is None:
        #guardar datos recibidos a la tabla User
        new_user = User(email=body["email"],password=body["password"])
        db.session.add(new_user)
        db.session.commit()
        response_body = {
                "msg": "created user"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "existed user"
        }
    return jsonify(response_body), 400

##------------------------------------------------Personajes
@app.route('/personajes', methods=['GET'])
def get_all_personajes():
    personajes = Personaje.query.all() # esto obtiene todos los registros de la tabla Personaje
    results = list(map(lambda item: item.serialize(), personajes)) #esto serializa los datos del arrays personajes

    return jsonify(results), 200

@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def get_personaje(personaje_id):

    personaje = Personaje.query.filter_by(id=personaje_id).first()

    return jsonify(personaje.serialize()), 200

##------------------------------------------------Planetas
@app.route('/planetas', methods=['GET'])
def get_all_planetas():
    planetas = Planeta.query.all() # esto obtiene todos los registros de la tabla Planetas
    results = list(map(lambda item: item.serialize(), planetas)) #esto serializa los datos del arrays Planetas

    return jsonify(results), 200

@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def get_planeta(planeta_id):

    planeta = Planeta.query.filter_by(id=planeta_id).first()

    return jsonify(planeta.serialize()), 200

##------------------------------------------------Favoritos
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet_to_user(planet_id):
    body = json.loads(request.data)

    query_favorite = Planeta.query.filter_by(id=planet_id).first()
    print(query_favorite)
    
    if query_favorite is not None:
        #guardar datos recibidos a la tabla Favorito
        new_favorite = Favorito(user_id=1,planetas_id=planet_id,personajes_id=None)
        db.session.add(new_favorite)
        db.session.commit()
        response_body = {
                "msg": "created favorite"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "Not exist planet"
        }
    return jsonify(response_body), 400

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people_to_user(people_id):
    body = json.loads(request.data)

    query_favorite = Personaje.query.filter_by(id=people_id).first()
    print(query_favorite)
    
    if query_favorite is not None:
        #guardar datos recibidos a la tabla Favorito
        new_favorite = Favorito(user_id=1,planetas_id=None,personajes_id=people_id)
        db.session.add(new_favorite)
        db.session.commit()
        response_body = {
                "msg": "created favorite"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "Not exist people"
        }
    return jsonify(response_body), 400

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    body = json.loads(request.data)

    query_favorite = Favorito.query.filter_by(planetas_id=planet_id).first()
    print(query_favorite)
    
    if query_favorite is not None:
        #guardar datos recibidos a la tabla Favorito
        db.session.delete(query_favorite)
        db.session.commit()
        response_body = {
                "msg": "deleted favorite"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "Not exist planet"
        }
    return jsonify(response_body), 400

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    body = json.loads(request.data)

    query_favorite = Favorito.query.filter_by(personajes_id=people_id).first()
    print(query_favorite)
    
    if query_favorite is not None:
        #guardar datos recibidos a la tabla Favorito
        db.session.delete(query_favorite)
        db.session.commit()
        response_body = {
                "msg": "deleted favorite"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "Not exist people"
        }
    return jsonify(response_body), 400

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
