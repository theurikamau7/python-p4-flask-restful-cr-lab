#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image = db.Column(db.String(255))
    price = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'price': self.price
        }


@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    plant_list = [plant.to_dict() for plant in plants]
    return jsonify(plant_list)


@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    name = data.get('name')
    image = data.get('image')
    price = data.get('price')

    plant = Plant(name=name, image=image, price=price)
    db.session.add(plant)
    db.session.commit()

    return jsonify(plant.to_dict()), 201


@app.route('/plants/<int:plant_id>', methods=['GET'])
def get_plant(plant_id):
    plant = Plant.query.get(plant_id)
    if plant:
        return jsonify(plant.to_dict())
    else:
        return jsonify({'message': 'Plant not found'}), 404


if __name__ == '__main__':
    db.init_app(app)  # Initialize the SQLAlchemy app
    app.run(port=5555, debug=True)
