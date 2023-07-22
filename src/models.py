from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    # planets_id = db.relationship('Planet', lazy=True)
    # people_id = db.relationship('People', lazy=True)
    def __repr__(self):
        return '<User %r>' % self.email
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class UserFavorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    planets_id = db.relationship('Planet', lazy=True)
    people_id = db.relationship('People', lazy=True)
    def __repr__(self):
        return '<UserFavorites %r>' % self.id
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planets": [Planet.serialize() for Planet in self.planets_id],
            "people": [People.serialize() for People in self.people_id],
            # do not serialize the password, its a security breach
        }
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=True)
    diameter = db.Column(db.Integer, unique=False, nullable=True)
    gravity = db.Column(db.Integer, unique=False, nullable=True)
    orbital_period = db.Column(db.Integer, unique=False, nullable=True)
    climate = db.Column(db.String(80), unique=False, nullable=True)
    terrain = db.Column(db.String(80), unique=False, nullable=True)
    favorite_planets = db.Column(db.Integer, db.ForeignKey(UserFavorites.id))
    def __repr__(self):
        return '<Planet %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mass": self.mass,
            # "diameter": self.diameter,
            # "gravity": self.gravity,
            # "orbital_period": self.orbital_period,
            # "climate": self.climate,
            # "terrain": self.terrain,
        }
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=True)
    height = db.Column(Integer, unique=False, nullable=True)
    weight = db.Column(Integer, unique=False, nullable=True)
    age = db.Column(Integer, unique=False, nullable=True)
    race = db.Column(db.String(80), unique=False, nullable=True)
    hair_color = db.Column(db.String(80), unique=False, nullable=True)
    eye_color = db.Column(db.String(80), unique=False, nullable=True)
    favorite_people = db.Column(db.Integer, db.ForeignKey(UserFavorites.id))
    def __repr__(self):
        return '<People %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # "gender": self.gender,
            # "height": self.height,
            # "weight": self.weight,
            # "age": self.age,
            # "race": self.race,
            # "hair_color": self.hair_color,
            # "eye_color": self.eye_color,
        }