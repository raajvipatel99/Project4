from collections import OrderedDict

from app import db

class Biostat(db.Model):
    __tablename__ = 'biostat'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(20), unique=False, nullable=False)
    sex = db.Column(db.String(3), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    height_in = db.Column(db.Integer, unique=False, nullable=False)
    weight_lbs = db.Column(db.Integer, unique=False, nullable=False)

    def toDict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
              result[key] = str(getattr(self, key))
        return result

    def __repr__(self):
        return '<Name %r>' % self.names

class Signup(db.Model):
    __tablename__ = 'signup'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)