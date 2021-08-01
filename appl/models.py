from app import db

class Biostat(db.Model):
    __tablename__ = 'biostat'
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(20), unique=False, nullable=False)
    sex = db.Column(db.String(3), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    height_in = db.Column(db.Integer, unique=False, nullable=False)
    weight_lbs = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.names