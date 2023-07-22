"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, UserFavorites, Planet, People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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



@app.route('/users', methods=['GET'])
def get_users():
    
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

@app.route('/user', methods=['POST'])
def create_user():
    
    request_body_user = request.get_json()
    new_user = User(username=request_body_user["username"], password=request_body_user["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(request_body_user), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    
    request_body_user = request.get_json()
    
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    
    if "username" in request_body_user:
        user1.username = request_body_user["username"]
    if "password" in request_body_user:
        user1.password = request_body_user["password"]
    db.session.commit()
    
    return jsonify(request_body_user), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()
    
    return jsonify("OK"), 200


@app.route('/people', methods=['GET'])
def get_all_people():
    
    people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people))

    return jsonify(all_people), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    
    people = People.query.filter_by(id=people_id).first()
    

    return jsonify(people.serialize()), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorite():
    # create_user = User.query.filter_by(id=user_id).first()
    favorite_list = UserFavorites.query.all()
    favorite_serialized = [item.serialize() for item in favorite_list]
    return jsonify(favorite_serialized), 200


@app.route('/planet', methods=['GET'])
def get_all_planet():
    
    planet = Planet.query.all()
    all_planet = list(map(lambda x: x.serialize(), planet))

    return jsonify(all_planet), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    
    planet = Planet.query.filter_by(id=planet_id).first()
    

    return jsonify(planet.serialize()), 200

# @app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
# def new_favorite_planet(planet_id):
#     request_body=request.get_json()
#     new_favorite_planet=UserFavorites(user_id = request_body["user_id"], planet_id=planet_id)
#     db.session.delete(new_favorite_planet)
#     db.session.commit()

#     return jsonify("planet favorite added"),200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def new_favorite_planet(planet_id):
    request_body = request.get_json()

    # Assuming you have a 'Planet' object with primary key 'planet_id'
    planet = Planet.query.get(planet_id)

    # Make sure the 'planet' object exists before proceeding
    if planet is None:
        return jsonify("Planet not found"), 404

    new_favorite_planet = UserFavorites(user_id=request_body["user_id"])
    new_favorite_planet.planets_id.append(planet)

    db.session.add(new_favorite_planet)
    db.session.commit()

    return jsonify("Planet favorite added"), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def new_favorite_people(people_id):
    request_body = request.get_json()

    # Assuming you have a 'Planet' object with primary key 'planet_id'
    people = People.query.get(people_id)

    # Make sure the 'planet' object exists before proceeding
    if people is None:
        return jsonify("people not found"), 404

    new_favorite_people = UserFavorites(user_id=request_body["user_id"])
    new_favorite_people.people_id.append(people)

    db.session.add(new_favorite_people)
    db.session.commit()

    return jsonify("People favorite added"), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    request_body = request.get_json()

    # Assuming you have a 'Planet' object with primary key 'planet_id'
    people = People.query.get(people_id)

    # Make sure the 'planet' object exists before proceeding
    if people is None:
        return jsonify("no favorite poeple to delete"), 404

     # Find the UserFavorites entry for the given user_id and planet_id
    favorite_people = UserFavorites.query.filter(UserFavorites.user_id == request_body["user_id"], UserFavorites.people_id.contains(people)).first()
    

    db.session.delete(favorite_people)
    db.session.commit()

    return jsonify("favorite people deleted"), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    request_body = request.get_json()

    # Assuming you have a 'Planet' object with primary key 'planet_id'
    planet = Planet.query.get(planet_id)

    # Make sure the 'planet' object exists before proceeding
    if planet is None:
        return jsonify("Planet not found"), 404

    # Find the UserFavorites entry for the given user_id and planet_id
    favorite_planet = UserFavorites.query.filter(UserFavorites.user_id == request_body["user_id"], UserFavorites.planets_id.contains(planet)).first()

    # If the favorite planet entry doesn't exist, return a 404 response
    if favorite_planet is None:
        return jsonify("Favorite planet not found"), 404

    # Delete the favorite planet entry from the database
    db.session.delete(favorite_planet)
    db.session.commit()

    return jsonify("Favorite planet deleted"), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
