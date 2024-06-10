import unittest
from sportsapp import create_app
from sportsapp.database import db
from sportsapp.models import Sport, Event, Selection
from datetime import datetime
import json


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

        # Ensure a clean state before each test
        with self.app.application.app_context():
            db.drop_all()
            db.create_all()  # Ensure all tables are created
            # Add a sport for event creation tests
            sport = Sport(name="Cricket", slug="cricket", active=True)
            db.session.add(sport)
            db.session.commit()
            self.sport_id = sport.id
            print(f"Sport created with ID: {self.sport_id}")

            # Add events
            event1 = Event(name="Cricket Match", slug="cricket-match", active=True, type="preplay",
                           sport_id=self.sport_id, status="Pending",
                           scheduled_start=datetime.strptime("2023-06-10T20:00:00", "%Y-%m-%dT%H:%M:%S"))
            db.session.add(event1)
            db.session.commit()

            # Add selections for event1
            selection1 = Selection(name="1", event_id=event1.id, price=1.63, active=True, outcome="Unsettled")
            selection2 = Selection(name="X", event_id=event1.id, price=4.20, active=True, outcome="Unsettled")
            selection3 = Selection(name="2", event_id=event1.id, price=5.00, active=True, outcome="Unsettled")
            db.session.add(selection1)
            db.session.add(selection2)
            db.session.add(selection3)
            db.session.commit()

    def tearDown(self):
        # Drop the database
        with self.app.application.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_sport(self):
        response = self.app.post('/sports/', data=json.dumps({
            "name": "Rugby",
            "slug": "rugby",
            "active": True
        }), content_type='application/json')
        print("Create Sport Response:", response.json)  # Log the response for debugging
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Rugby")

    def test_create_event(self):
        response = self.app.post('/events/', data=json.dumps({
            "name": "Internazionale vs. Shakhtar Donetsk",
            "slug": "internazionale-vs-shakhtar-donetsk",
            "active": True,
            "type": "preplay",
            "sport_id": self.sport_id,
            "status": "Pending",
            "scheduled_start": "2023-06-10T20:00:00"
        }), content_type='application/json')
        print("Create Event Response:", response.json)  # Log the response for debugging
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Internazionale vs. Shakhtar Donetsk")

    def test_create_selections(self):
        # First, create an event for the selections to link to
        event_response = self.app.post('/events/', data=json.dumps({
            "name": "Internazionale vs. Shakhtar Donetsk",
            "slug": "internazionale-vs-shakhtar-donetsk",
            "active": True,
            "type": "preplay",
            "sport_id": self.sport_id,
            "status": "Pending",
            "scheduled_start": "2023-06-10T20:00:00"
        }), content_type='application/json')

        print("Create Event Response:", event_response.json)  # Log the response for debugging
        self.assertEqual(event_response.status_code, 201)

        event_id = event_response.json['id']

        # Create selections for the event
        selections = [
            {"name": "1", "event_id": event_id, "price": 1.63, "active": True, "outcome": "Unsettled"},
            {"name": "X", "event_id": event_id, "price": 4.20, "active": True, "outcome": "Unsettled"},
            {"name": "2", "event_id": event_id, "price": 5.00, "active": True, "outcome": "Unsettled"},
        ]

        for selection in selections:
            response = self.app.post('/selections/', data=json.dumps(selection), content_type='application/json')
            print("Create Selection Response:", response.json)  # Log the response for debugging
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json["name"], selection["name"])

    def test_search_sports(self):
        response = self.app.post('/sports/search', data=json.dumps({
            "name_regex": "Cricket",
            "min_active_events": 1,
            "min_active_selections": 1,
            "scheduled_start": ["2023-06-01T00:00:00", "2023-06-30T23:59:59"]
        }), content_type='application/json')
        print("Search Sports Response:", response.json)  # Log the response for debugging
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)

    def test_search_events(self):
        response = self.app.post('/events/search', data=json.dumps({
            "name_regex": "Cricket",
            "min_active_events": 1,
            "min_active_selections": 1,
            "scheduled_start": ["2023-06-01T00:00:00", "2023-06-30T23:59:59"]
        }), content_type='application/json')
        print("Search Events Response:", response.json)  # Log the response for debugging
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)

    def test_search_selections(self):
        response = self.app.post('/selections/search', data=json.dumps({
            "name_regex": "X",
            "min_active_events": 1,
            "min_active_selections": 1,
            "scheduled_start": ["2023-06-01T00:00:00", "2023-06-30T23:59:59"]
        }), content_type='application/json')
        print("Search Selections Response:", response.json)  # Log the response for debugging
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)

    def test_update_sport(self):
        response = self.app.put(f'/sports/{self.sport_id}', data=json.dumps({
            "name": "Updated Cricket",
            "slug": "updated-cricket",
            "active": False
        }), content_type='application/json')
        print("Update Sport Response:", response.json)  # Log the response for debugging
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Updated Cricket")
        self.assertEqual(response.json["active"], False)

    def test_update_event(self):
        event_response = self.app.post('/events/', data=json.dumps({
            "name": "Cricket Match ",
            "slug": "cricket-match-1",
            "active": True,
            "type": "preplay",
            "sport_id": self.sport_id,
            "status": "Pending",
            "scheduled_start": "2023-06-10T20:00:00"
        }), content_type='application/json')
        event_id = event_response.json['id']
        response = self.app.put(f'/events/{event_id}', data=json.dumps({
            "name": "Updated Match",
            "slug": "updated-match",
            "active": True,
            "type": "preplay",
            "sport_id": self.sport_id,
            "status": "Started",
            "scheduled_start": "2023-06-10T20:00:00"
        }), content_type='application/json')
        print("Update Event Response:", response.json)  # Log the response for debugging
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Updated Match")
        self.assertEqual(response.json["status"], "Started")

    def test_update_selection(self):
        # First, create an event
        event_response = self.app.post('/events/', data=json.dumps({
            "name": "Internazionale vs. Shakhtar Donetsk",
            "slug": "internazionale-vs-shakhtar-donetsk",
            "active": True,
            "type": "preplay",
            "sport_id": self.sport_id,
            "status": "Pending",
            "scheduled_start": "2023-06-10T20:00:00"
        }), content_type='application/json')

        # Check event creation response
        self.assertEqual(event_response.status_code, 201)
        event_id = event_response.json['id']
        # Create a selection for the event
        selection_response = self.app.post('/selections/', data=json.dumps({
            "name": "1",
            "event_id": event_id,
            "price": 1.63,
            "active": True,
            "outcome": "Unsettled"
        }), content_type='application/json')
        # Check selection creation response
        self.assertEqual(selection_response.status_code, 201)
        selection_id = selection_response.json['id']
        # Update the selection
        response = self.app.put(f'/selections/{selection_id}', data=json.dumps({
            "name": "Updated Selection",
            "active": False,
            "event_id": event_id,
            "price": 1.63,
            "outcome": "Unsettled"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200, msg=f"Selection update failed: {response.json}")
        self.assertEqual(response.json["name"], "Updated Selection")
        self.assertEqual(response.json["active"], False)

        # Ensure all selections for the event are inactive
        selection_response = self.app.put(f'/selections/{selection_id}', data=json.dumps({
            "active": False
        }), content_type='application/json')

        # Get the event to verify it becomes inactive
        event_response = self.app.get(f'/events/{event_id}')
        # Check event response and status
        self.assertEqual(event_response.status_code, 200, msg=f"Event retrieval failed: {event_response.json}")
        self.assertEqual(event_response.json["active"], 0)

    def test_get_sports(self):
        response = self.app.get('/sports')
        print("Get Sports Response:", response.json)  # Log the response for debugging
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)
        self.assertIn('events', response.json[0])

    def test_get_events(self):
        response = self.app.get('/events')
        print("Get Events Response:", response.json)  # Log the response for debugging
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)
        self.assertIn('selections', response.json[0])

    def test_get_selections(self):
        response = self.app.get('/selections')
        print("Get Selections Response:", response.json)  # Log the response for debugging
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)


if __name__ == '__main__':
    unittest.main()
