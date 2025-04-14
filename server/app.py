from flask import Flask, jsonify, request
from flask_migrate import Migrate
import os
from models import db, Episode, Guest, Appearance


instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "lateshow.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([e.to_dict() for e in episodes])

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if episode:
        return jsonify(episode.to_dict_with_appearances())
    return jsonify({"error": "Episode not found"}), 404

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([g.to_dict() for g in guests])

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    
    if not data:
        return jsonify({"errors": ["No data provided"]}), 400
    
    rating = data.get('rating')
    episode_id = data.get('episode_id')
    guest_id = data.get('guest_id')

    # Validating required fields
    if None in (rating, episode_id, guest_id):
        return jsonify({"errors": ["Missing required fields"]}), 400

    # Validating rating
    if not (1 <= rating <= 5):
        return jsonify({"errors": ["Rating must be between 1 and 5"]}), 400

    # Checking if episode exists
    if not Episode.query.get(episode_id):
        return jsonify({"errors": ["Episode not found"]}), 404

    # Checking if guest exists
    if not Guest.query.get(guest_id):
        return jsonify({"errors": ["Guest not found"]}), 404

    try:
        appearance = Appearance(
            rating=rating,
            episode_id=episode_id,
            guest_id=guest_id
        )
        db.session.add(appearance)
        db.session.commit()
        return jsonify(appearance.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5555)