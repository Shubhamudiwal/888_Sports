from sportsapp.database import db


class Sport(db.Model):
    """
        Sport model representing a sport entity in the database.

        Attributes:
            id (int): The primary key of the sport.
            name (str): The name of the sport.
            slug (str): A unique slug for the sport.
            active (bool): Indicates whether the sport is active.
            events (list[Event]): A list of events associated with the sport.
        """
    __tablename__ = 'sports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    events = db.relationship('Event', backref='sport', lazy=True)

    def to_dict(self):
        """
                Convert the Sport instance to a dictionary.

                Returns:
                    dict: A dictionary representation of the Sport instance.
        """
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'active': self.active,
            'events': [event.to_dict() for event in self.events]
        }


class Event(db.Model):
    """
        Event model representing an event entity in the database.

        Attributes:
            id (int): The primary key of the event.
            name (str): The name of the event.
            slug (str): A unique slug for the event.
            active (bool): Indicates whether the event is active.
            type (str): The type of the event.
            sport_id (int): The ID of the sport associated with the event.
            status (str): The status of the event.
            scheduled_start (datetime): The scheduled start time of the event.
            actual_start (datetime): The actual start time of the event.
            selections (list[Selection]): A list of selections associated with the event.
    """
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
        """
                Convert the Event instance to a dictionary.

                Returns:
                    dict: A dictionary representation of the Event instance.
        """
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
    """
        Selection model representing a selection entity in the database.

        Attributes:
            id (int): The primary key of the selection.
            name (str): The name of the selection.
            event_id (int): The ID of the event associated with the selection.
            price (Decimal): The price of the selection.
            active (bool): Indicates whether the selection is active.
            outcome (str): The outcome status of the selection.
    """
    __tablename__ = 'selections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    active = db.Column(db.Boolean, default=True)
    outcome = db.Column(db.String, nullable=False)

    def to_dict(self):
        """
                Convert the Selection instance to a dictionary.

                Returns:
                    dict: A dictionary representation of the Selection instance.
        """
        return {
            'id': self.id,
            'name': self.name,
            'event_id': self.event_id,
            'price': str(self.price),
            'active': self.active,
            'outcome': self.outcome
        }
