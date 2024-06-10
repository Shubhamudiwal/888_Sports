from sportsapp.database import db


class Sport(db.Model):
    __tablename__ = 'sports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    events = db.relationship('Event', backref='sport', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'active': self.active,
            'events': [event.to_dict() for event in self.events]
        }


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
    selections = db.relationship('Selection', backref='event', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'active': self.active,
            'type': self.type,
            'sport_id': self.sport_id,
            'status': self.status,
            'scheduled_start': self.scheduled_start,
            'actual_start': self.actual_start,
            'selections': [selection.to_dict() for selection in self.selections]
        }


class Selection(db.Model):
    __tablename__ = 'selections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    active = db.Column(db.Boolean, default=True)
    outcome = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'event_id': self.event_id,
            'price': str(self.price),
            'active': self.active,
            'outcome': self.outcome
        }
