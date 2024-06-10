from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sportsapp import crud, schemas, models
from sportsapp.database import db

main = Blueprint('main', __name__)

@main.route('/sports/', methods=['POST'])
def create_sport():
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
    try:
        event = crud.get_event(event_id)
        if event:
            return jsonify(dict(event)), 200
        return jsonify({"error": "Event not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@main.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
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

