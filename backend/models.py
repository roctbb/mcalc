from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# models
class Calc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=True)
    payload = db.Column(db.JSON, nullable=True)

    def as_dict(self, native=False):
        serialized = {
            "id": self.id,
            "title": self.title,
            "payload": self.payload,
        }

        return serialized
