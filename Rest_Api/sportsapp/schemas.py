from pydantic import BaseModel
from typing import Optional, List


class SportCreate(BaseModel):
    """
        Pydantic model for creating a new sport.

        Attributes:
            name (str): The name of the sport.
            slug (str): The slug for the sport.
            active (bool): The active status of the sport.
    """
    name: str
    slug: str
    active: bool


class SportUpdate(BaseModel):
    """
        Pydantic model for updating an existing sport.

        Attributes:
            name (Optional[str]): The updated name of the sport.
            slug (Optional[str]): The updated slug for the sport.
            active (Optional[bool]): The updated active status of the sport.
    """
    name: Optional[str]
    slug: Optional[str]
    active: Optional[bool]


class EventCreate(BaseModel):
    """
        Pydantic model for creating a new event.

        Attributes:
            name (str): The name of the event.
            slug (str): The slug for the event.
            active (bool): The active status of the event.
            type (str): The type of the event.
            sport_id (int): The ID of the sport associated with the event.
            status (str): The status of the event.
            scheduled_start (str): The scheduled start time of the event.
            actual_start (Optional[str]): The actual start time of the event (default is None).
    """
    name: str
    slug: str
    active: bool
    type: str
    sport_id: int
    status: str
    scheduled_start: str
    actual_start: Optional[str] = None


class EventUpdate(BaseModel):
    """
        Pydantic model for updating an existing event.

        Attributes:
            name (Optional[str]): The updated name of the event.
            slug (Optional[str]): The updated slug for the event.
            active (Optional[bool]): The updated active status of the event.
            type (Optional[str]): The updated type of the event.
            sport_id (Optional[int]): The updated ID of the sport associated with the event.
            status (Optional[str]): The updated status of the event.
            scheduled_start (Optional[str]): The updated scheduled start time of the event.
            actual_start (Optional[str]): The updated actual start time of the event (default is None).
    """
    name: Optional[str]
    slug: Optional[str]
    active: Optional[bool]
    type: Optional[str]
    sport_id: Optional[int]
    status: Optional[str]
    scheduled_start: Optional[str]
    actual_start: Optional[str] = None


class SelectionCreate(BaseModel):
    """
        Pydantic model for creating a new selection.

        Attributes:
            name (str): The name of the selection.
            event_id (int): The ID of the event associated with the selection.
            price (float): The price of the selection.
            active (bool): The active status of the selection.
            outcome (str): The outcome status of the selection.
    """
    name: str
    event_id: int
    price: float
    active: bool
    outcome: str


class SelectionUpdate(BaseModel):
    """
        Pydantic model for updating an existing selection.

        Attributes:
            name (Optional[str]): The updated name of the selection.
            event_id (Optional[int]): The updated ID of the event associated with the selection.
            price (Optional[float]): The updated price of the selection.
            active (Optional[bool]): The updated active status of the selection.
            outcome (Optional[str]): The updated outcome status of the selection.
    """
    name: Optional[str]
    event_id: Optional[int]
    price: Optional[float]
    active: Optional[bool]
    outcome: Optional[str]


class Filter(BaseModel):
    """
        Pydantic model for filtering sports, events, and selections.

        Attributes:
            name_regex (Optional[str]): A regex pattern to filter by name.
            min_active_events (Optional[int]): The minimum number of active events.
            min_active_selections (Optional[int]): The minimum number of active selections.
            scheduled_start (Optional[List[str]]): A list with the start and end time to filter events by scheduled start time.
    """
    name_regex: Optional[str]
    min_active_events: Optional[int]
    min_active_selections: Optional[int]
    scheduled_start: Optional[List[str]]
