# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'qlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake is None:
        return jsonify({'message': f'Earthquake {id} not found.'}), 404
    return jsonify({
        'id': earthquake.id,
        'location': earthquake.location,
        'agnitude': earthquake.magnitude,
        'year': earthquake.year
    }), 200


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(earthquakes)
    quakes = [{
        'id': e.id,
        'location': e.location,
        'agnitude': e.magnitude,
        'year': e.year
    } for e in earthquakes]
    return jsonify({'count': count, 'quakes': quakes}), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)