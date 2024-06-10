from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sportsapp import crud, schemas, models
from sportsapp.database import db

main = Blueprint('main', __name__)


@main.route('/sports/', methods=['POST'])
def create_sport():
    """
        Create a new sport.

        Request Body:
        - name: The name of the sport (str)
        - slug: A unique slug for the sport (str)
        - active: The active status of the sport (bool)

        Returns:
        - 201: Sport created successfully
        - 400: Validation or creation error
    """
    data = request.get_json()
    try:
        sport = schemas.SportCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    try:
        crud.create_sport(sport)
        db.session.commit()
    except Exception as e:
        print(f"Error creating sport: {e}")
        return jsonify({"error": str(e)}), 400
    return jsonify(sport.dict()), 201


@main.route('/sports/<int:sport_id>', methods=['PUT'])
def update_sport(sport_id):
    """
        Update an existing sport.

        Parameters:
        - sport_id: The ID of the sport to update (int)

        Request Body:
        - name: The name of the sport (str, optional)
        - slug: A unique slug for the sport (str, optional)
        - active: The active status of the sport (bool, optional)

        Returns:
        - 200: Sport updated successfully
        - 400: Validation or update error
    """
    data = request.get_json()
    try:
        sport_data = schemas.SportUpdate(**data).dict(exclude_unset=True)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    try:
        crud.update_sport(sport_id, sport_data)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"id": sport_id, **sport_data}), 200


@main.route('/sports/search', methods=['POST'])
def search_sports():
    """
        Search for sports based on filters.

        Request Body:
        - name_regex: Regex pattern to match sport names (str, optional)
        - min_active_events: Minimum number of active events (int, optional)

        Returns:
        - 200: List of sports matching the filters
        - 400: Validation or search error
    """
    data = request.get_json()
    try:
        filters = schemas.Filter(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    try:
        sports = crud.search_sports(filters)
        return jsonify([dict(row) for row in sports]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@main.route('/events/', methods=['POST'])
def create_event():
    """
        Create a new event.

        Request Body:
        - name: The name of the event (str)
        - slug: A unique slug for the event (str)
        - active: The active status of the event (bool)
        - type: The type of the event (str)
        - sport_id: The ID of the sport associated with the event (int)
        - status: The status of the event (str)
        - scheduled_start: The scheduled start time of the event (str, datetime format)
        - actual_start: The actual start time of the event (str, datetime format, optional)

        Returns:
        - 201: Event created successfully
        - 400: Validation or creation error
    """
    data = request.get_json()
    try:
        event = schemas.EventCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    sport = crud.get_sport(event.sport_id)
    if sport is None:
        return jsonify({"error": f"Sport with id {event.sport_id} does not exist"}), 400

    try:
        event_id = crud.create_event(event)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    event_dict = event.dict()
    event_dict['id'] = event_id
    return jsonify(event_dict), 201


@main.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """
        Retrieve an event by ID.

        Parameters:
        - event_id: The ID of the event to retrieve (int)

        Returns:
        - 200: Event retrieved successfully
        - 404: Event not found
        - 400: Retrieval error
    """
    try:
        event = crud.get_event(event_id)
        if event:
            return jsonify(dict(event)), 200
        return jsonify({"error": "Event not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@main.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """
        Update an existing event.

        Parameters:
        - event_id: The ID of the event to update (int)

        Request Body:
        - name: The name of the event (str, optional)
        - slug: A unique slug for the event (str, optional)
        - active: The active status of the event (bool, optional)
        - type: The type of the event (str, optional)
        - sport_id: The ID of the sport associated with the event (int, optional)
        - status: The status of the event (str, optional)
        - scheduled_start: The scheduled start time of the event (str, datetime format, optional)
        - actual_start: The actual start time of the event (str, datetime format, optional)

        Returns:
        - 200: Event updated successfully
        - 400: Validation or update error
    """
    data = request.get_json()
    try:
        event_data = schemas.EventUpdate(**data).dict(exclude_unset=True)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    try:
        crud.update_event(event_id, event_data)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"id": event_id, **event_data}), 200


@main.route('/events/search', methods=['POST'])
def search_events():
    """
        Search for events based on filters.

        Request Body:
        - name_regex: Regex pattern to match event names (str, optional)
        - min_active_events: Minimum number of active events (int, optional)
        - min_active_selections: Minimum number of active selections (int, optional)
        - scheduled_start: Time range for scheduled start (list of two str, datetime format, optional)

        Returns:
        - 200: List of events matching the filters
        - 400: Validation or search error
    """
    data = request.get_json()
    try:
        filters = schemas.Filter(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    try:
        events = crud.search_events(filters)
        return jsonify([dict(row) for row in events]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@main.route('/selections/', methods=['POST'])
def create_selection():
    """
        Create a new selection.

        Request Body:
        - name: The name of the selection (str)
        - event_id: The ID of the event associated with the selection (int)
        - price: The price of the selection (decimal)
        - active: The active status of the selection (bool)
        - outcome: The outcome status of the selection (str)

        Returns:
        - 201: Selection created successfully
        - 400: Validation or creation error
    """
    data = request.get_json()
    try:
        selection = schemas.SelectionCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    event = crud.get_event(selection.event_id)
    if event is None:
        return jsonify({"error": f"Event with id {selection.event_id} does not exist"}), 400

    try:
        selection_id = crud.create_selection(selection)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    selection_dict = selection.dict()
    selection_dict['id'] = selection_id
    return jsonify(selection_dict), 201


@main.route('/selections/<int:selection_id>', methods=['PUT'])
def update_selection(selection_id):
    """
        Update an existing selection.

        Parameters:
        - selection_id: The ID of the selection to update (int)

        Request Body:
        - name: The name of the selection (str, optional)
        - event_id: The ID of the event associated with the selection (int, optional)
        - price: The price of the selection (decimal, optional)
        - active: The active status of the selection (bool, optional)
        - outcome: The outcome status of the selection (str, optional)

        Returns:
        - 200: Selection updated successfully
        - 400: Validation or update error
    """
    data = request.get_json()
    try:
        selection_data = schemas.SelectionUpdate(**data).dict(exclude_unset=True)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    try:
        crud.update_selection(selection_id, selection_data)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"id": selection_id, **selection_data}), 200


@main.route('/selections/search', methods=['POST'])
def search_selections():
    """
        Search for selections based on filters.

        Request Body:
            - name_regex: str (optional)
            - min_active_events: int (optional)
            - min_active_selections: int (optional)
            - scheduled_start: list[str] (optional)

        Returns:
            JSON response containing a list of selections matching the filters or error message.
    """
    data = request.get_json()
    try:
        filters = schemas.Filter(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    try:
        selections = crud.search_selections(filters)
        return jsonify([dict(row) for row in selections]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@main.route('/sports', methods=['GET'])
def get_sports():
    """
        Retrieve all sports.

        Returns:
            JSON response containing a list of all sports.
    """
    sports = crud.get_all_sports()
    return jsonify([sport.to_dict() for sport in sports])


@main.route('/events', methods=['GET'])
def get_events():
    """
        Retrieve all events.

        Returns:
            JSON response containing a list of all events.
    """
    events = crud.get_all_events()
    return jsonify([event.to_dict() for event in events])


@main.route('/selections', methods=['GET'])
def get_selections():
    """
        Retrieve all selections.

        Returns:
            JSON response containing a list of all selections.
    """
    selections = crud.get_all_selections()
    return jsonify([selection.to_dict() for selection in selections])
