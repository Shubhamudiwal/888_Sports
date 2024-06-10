from sqlalchemy import text
from sportsapp.database import db
from sportsapp.models import Sport, Event, Selection


def create_sport(sport):
    """
        Create a new sport in the database.

        Args:
            sport (SportCreate): The sport data to be inserted.

    """
    with db.engine.connect() as conn:
        conn.execute(
            text('INSERT INTO sports (name, slug, active) VALUES (:name, :slug, :active)'),
            {"name": sport.name, "slug": sport.slug, "active": sport.active}
        )
        conn.commit()


def create_event(event):
    """
        Create a new event in the database.

        Args:
            event (EventCreate): The event data to be inserted.

        Returns:
            int: The ID of the created event.
        """
    with db.engine.connect() as conn:
        result = conn.execute(
            text(
                'INSERT INTO events (name, slug, active, type, sport_id, status, scheduled_start, actual_start) VALUES (:name, :slug, :active, :type, :sport_id, :status, :scheduled_start, :actual_start)'),
            {"name": event.name, "slug": event.slug, "active": event.active, "type": event.type,
             "sport_id": event.sport_id, "status": event.status, "scheduled_start": event.scheduled_start,
             "actual_start": event.actual_start}
        )
        event_id = result.lastrowid
        conn.commit()
    return event_id


def create_selection(selection):
    """
        Create a new selection in the database.

        Args:
            selection (SelectionCreate): The selection data to be inserted.

        Returns:
            int: The ID of the created selection.
    """
    with db.engine.connect() as conn:
        result = conn.execute(
            text(
                'INSERT INTO selections (name, event_id, price, active, outcome) VALUES (:name, :event_id, :price, :active, :outcome)'),
            {"name": selection.name, "event_id": selection.event_id, "price": selection.price,
             "active": selection.active, "outcome": selection.outcome}
        )
        selection_id = result.lastrowid
        conn.commit()
    # Check and update event status if necessary
    check_event_status(selection.event_id)
    return selection_id


def get_sport(sport_id):
    """
        Retrieve a sport from the database by its ID.

        Args:
            sport_id (int): The ID of the sport.

        Returns:
            dict: The sport data as a dictionary.
    """
    with db.engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM sports WHERE id = :id'), {"id": sport_id})
        sport = result.fetchone()
        if sport:
            return dict(sport._mapping)
        return None


def get_event(event_id):
    """
        Retrieve an event from the database by its ID.

        Args:
            event_id (int): The ID of the event.

        Returns:
            dict: The event data as a dictionary.
    """
    with db.engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM events WHERE id = :id'), {"id": event_id})
        event = result.fetchone()
    if event:
        return dict(event._mapping)  # Convert RowProxy to dict
    return None


def get_selection(selection_id):
    """
        Retrieve a selection from the database by its ID.

        Args:
            selection_id (int): The ID of the selection.

        Returns:
            dict: The selection data as a dictionary.
    """
    with db.engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM selections WHERE id = :id'), {"id": selection_id})
        selection = result.fetchone()
    return selection


def search_sports(filters):
    """
        Search for sports based on the provided filters.

        Args:
            filters (Filter): The search filters.

        Returns:
            list: A list of sports matching the filters.
    """
    query = 'SELECT * FROM sports WHERE 1=1'
    params = {}

    if filters.name_regex:
        query += ' AND name REGEXP :name_regex'
        params['name_regex'] = filters.name_regex
    if filters.min_active_events is not None:
        query += ' AND (SELECT COUNT(*) FROM events WHERE sport_id = sports.id AND active = 1) >= :min_active_events'
        params['min_active_events'] = filters.min_active_events

    with db.engine.connect() as conn:
        result = conn.execute(text(query), params)
        sports = [dict(row._mapping) for row in result]
        # sports = result.fetchall()
    return sports


def search_events(filters):
    """
        Search for events based on the provided filters.

        Args:
            filters (Filter): The search filters.

        Returns:
            list: A list of events matching the filters.
    """
    query = 'SELECT * FROM events WHERE 1=1'
    params = {}

    if filters.name_regex:
        query += " AND name REGEXP :name_regex"
        params['name_regex'] = filters.name_regex

    if filters.min_active_events:
        query += """ AND (SELECT COUNT(*) FROM events e WHERE e.sport_id = events.sport_id AND e.active = TRUE) >= :min_active_events"""
        params['min_active_events'] = filters.min_active_events

    if filters.min_active_selections:
        query += """ AND (SELECT COUNT(*) FROM selections s WHERE s.event_id = events.id AND s.active = TRUE) >= :min_active_selections"""
        params['min_active_selections'] = filters.min_active_selections

    if filters.scheduled_start:
        start, end = filters.scheduled_start
        query += " AND scheduled_start BETWEEN :start AND :end"
        params['start'] = start
        params['end'] = end

    with db.engine.connect() as conn:
        result = conn.execute(text(query), params)
        events = [dict(row._mapping) for row in result]
    return events


def search_selections(filters):
    """
        Search for selections based on the provided filters.

        Args:
            filters (Filter): The search filters.

        Returns:
            list: A list of selections matching the filters.
    """
    query = 'SELECT * FROM selections WHERE 1=1'
    params = {}

    if filters.name_regex:
        query += " AND name REGEXP :name_regex"
        params['name_regex'] = filters.name_regex

    if filters.min_active_events:
        query += """ AND (SELECT COUNT(*) FROM events e WHERE e.sport_id = selections.event_id AND e.active = TRUE) >= :min_active_events"""
        params['min_active_events'] = filters.min_active_events

    if filters.min_active_selections:
        query += """ AND (SELECT COUNT(*) FROM selections s WHERE s.event_id = selections.event_id AND s.active = TRUE) >= :min_active_selections"""
        params['min_active_selections'] = filters.min_active_selections

    if filters.scheduled_start:
        start, end = filters.scheduled_start
        query += """ AND (SELECT scheduled_start FROM events e WHERE e.id = selections.event_id) BETWEEN :start AND :end"""
        params['start'] = start
        params['end'] = end

    with db.engine.connect() as conn:
        result = conn.execute(text(query), params)
        selections = [dict(row._mapping) for row in result]
    return selections


def update_sport(sport_id, sport_data):
    """
        Update a sport in the database.

        Args:
            sport_id (int): The ID of the sport to update.
            sport_data (dict): The updated sport data.
    """
    set_clause = ', '.join([f"{k} = :{k}" for k in sport_data.keys()])
    sport_data['id'] = sport_id
    with db.engine.connect() as conn:
        conn.execute(
            text(f'UPDATE sports SET {set_clause} WHERE id = :id'),
            sport_data
        )
        conn.commit()


def update_event(event_id, event_data):
    """
        Update an event in the database.

        Args:
            event_id (int): The ID of the event to update.
            event_data (dict): The updated event data.
    """
    set_clause = ', '.join([f"{k} = :{k}" for k in event_data.keys()])
    event_data['id'] = event_id
    with db.engine.connect() as conn:
        conn.execute(
            text(f'UPDATE events SET {set_clause} WHERE id = :id'),
            event_data
        )
        conn.commit()
    # Check and update sport status if necessary
    check_sport_status(event_data['id'])


def update_selection(selection_id, selection_data):
    """
        Update a selection in the database.

        Args:
            selection_id (int): The ID of the selection to update.
            selection_data (dict): The updated selection data.
    """
    set_clause = ', '.join([f"{k} = :{k}" for k in selection_data.keys()])
    selection_data['id'] = selection_id
    with db.engine.connect() as conn:
        conn.execute(
            text(f'UPDATE selections SET {set_clause} WHERE id = :id'),
            selection_data
        )
        conn.commit()
    check_event_status(selection_data['event_id'])


def check_event_status(event_id):
    """
        Check and update the status of an event based on its selections.

        Args:
            event_id (int): The ID of the event to check.
    """
    with db.engine.connect() as conn:
        active_selections = conn.execute(
            text('SELECT COUNT(*) FROM selections WHERE event_id = :event_id AND active = 1'),
            {"event_id": event_id}).scalar()
    if active_selections == 0:
        update_event(event_id, {"active": False})
        event = get_event(event_id)
        if event:
            check_sport_status(event['sport_id'])


def check_sport_status(sport_id):
    """
        Check and update the status of a sport based on its events.

        Args:
            sport_id (int): The ID of the sport to check.
    """
    with db.engine.connect() as conn:
        active_events = conn.execute(text('SELECT COUNT(*) FROM events WHERE sport_id = :sport_id AND active = 1'),
                                     {"sport_id": sport_id}).scalar()
    if active_events == 0:
        update_sport(sport_id, {"active": False})


def get_all_sports():
    """
        Retrieve all sports from the database.

        Returns:
            list: A list of all sports.
    """
    return Sport.query.all()


def get_all_events():
    """
        Retrieve all events from the database.

        Returns:
            list: A list of all events.
    """
    return Event.query.all()


def get_all_selections():
    """
        Retrieve all selections from the database.

        Returns:
            list: A list of all selections.
    """
    return Selection.query.all()
