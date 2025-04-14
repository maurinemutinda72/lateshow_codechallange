from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Episode(db.Model):
    __tablename__ = 'episodes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    appearances = db.relationship('Appearance', backref='episode', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "number": self.number
        }

    def to_dict_with_appearances(self):
        return {
            "id": self.id,
            "date": self.date,
            "number": self.number,
            "appearances": [{
                "id": appearance.id,
                "rating": appearance.rating,
                "episode_id": appearance.episode_id,
                "guest_id": appearance.guest_id,
                "guest": appearance.guest.to_dict()
            } for appearance in self.appearances]
        }

class Guest(db.Model):
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(50), nullable=False)
    appearances = db.relationship('Appearance', backref='guest', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "occupation": self.occupation
        }

class Appearance(db.Model):
    __tablename__ = 'appearances'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id', ondelete='CASCADE'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "guest_id": self.guest_id,
            "episode_id": self.episode_id,
            "episode": {
                "id": self.episode.id,
                "date": self.episode.date,
                "number": self.episode.number
            },
            "guest": self.guest.to_dict()
        }