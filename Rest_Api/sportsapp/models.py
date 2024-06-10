from sportsapp.database import db


class Sport(db.Model):
    __tablename__ = 'sports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    type = db.Column(db.String, nullable=False)
    sport_id = db.Column(db.Integer, db.ForeignKey('sports.id'), nullable=False)
    status = db.Column(db.String, nullable=False)
    scheduled_start = db.Column(db.DateTime, nullable=False)
    actual_start = db.Column(db.DateTime)


class Selection(db.Model):
    __tablename__ = 'selections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    active = db.Column(db.Boolean, default=True)
    outcome = db.Column(db.String, nullable=False)
