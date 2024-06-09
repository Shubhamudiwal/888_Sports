from pydantic import BaseModel, Field
from typing import Optional, List

class SportCreate(BaseModel):
    name: str
    slug: str
    active: bool

class SportUpdate(BaseModel):
    name: Optional[str]
    slug: Optional[str]
    active: Optional[bool]

class EventCreate(BaseModel):
    name: str
    slug: str
    active: bool
    type: str
    sport_id: int
    status: str
    scheduled_start: str
    actual_start: Optional[str] = None

class EventUpdate(BaseModel):
    name: Optional[str]
    slug: Optional[str]
    active: Optional[bool]
    type: Optional[str]
    sport_id: Optional[int]
    status: Optional[str]
    scheduled_start: Optional[str]
    actual_start: Optional[str] = None

class SelectionCreate(BaseModel):
    name: str
    event_id: int
    price: float
    active: bool
    outcome: str

class SelectionUpdate(BaseModel):
    name: Optional[str]
    event_id: Optional[int]
    price: Optional[float]
    active: Optional[bool]
    outcome: Optional[str]


class Filter(BaseModel):
    name_regex: Optional[str]
    min_active_events: Optional[int]
    min_active_selections: Optional[int]
    scheduled_start: Optional[List[str]]
