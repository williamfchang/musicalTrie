from flask_app import db

class MusicalWorkDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True)
    artist = db.Column(db.String(64))
    date = db.Column(db.DateTime)
    genre = db.Column(db.String(64))

    melody = db.Column(db.String(120), index=True, unique=True)
    key = db.Column(db.String(3))

    searchCount = db.Column(db.Integer)

    def __repr__(self):
        return f'<MusicalWorkDB {self.title}>'