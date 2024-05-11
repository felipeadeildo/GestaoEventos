from datetime import datetime
from decimal import Decimal
from typing import Annotated, List, Optional, Self

from prisma.bases import (
    BaseEvent,
    BaseEventSchedule,
    BaseFile,
    BaseParticipant,
    BaseTicket,
    BaseVenue,
)
from pydantic import BaseModel, Field, field_validator, model_validator


class File(BaseFile):
    id: str
    hash: str
    extension: str
    mime_type: str = Field(alias="mimeType")
    owner_id: str = Field(alias="ownerId")
    owner_type: str = Field(alias="ownerType")
    event_id: Optional[str] = Field(alias="eventId")
    event_schedule_id: Optional[str] = Field(alias="eventScheduleId")

    class Config:
        populate_by_name = True


class Ticket(BaseTicket):
    id: str
    event_id: str = Field(alias="eventId")
    price: Decimal
    start_date: datetime = Field(alias="startDate")
    end_date: datetime = Field(alias="endDate")
    avaiable: int = Field(alias="avaiable", ge=0)

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: Decimal):
        assert v > 0
        return v.quantize(Decimal("0.01"))

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        assert self.start_date < self.end_date
        return self

    class Config:
        populate_by_name = True


class EventSchedule(BaseEventSchedule):
    id: str
    event_id: str = Field(alias="eventId")
    start_date: datetime = Field(alias="startDate")
    end_date: datetime = Field(alias="endDate")
    files: List[File] = Field(default_factory=list)

    class Config:
        populate_by_name = True


class Venue(BaseVenue):
    id: str
    name: str = Field(max_length=100, min_length=1)
    capacity: int = Field(gt=0)
    address: str


class Event(BaseEvent):
    id: str
    title: Annotated[str, Field(max_length=100, min_length=1)]
    description: Optional[str] = Field(max_length=500)
    venue_id: str = Field(alias="venueId")
    schedules: List[EventSchedule]
    files: List[File] = Field(default_factory=list)
    tickets: List[Ticket] = Field(default_factory=list)

    class Config:
        populate_by_name = True


class Participant(BaseParticipant):
    id: str
    name: str = Field(max_length=100, min_length=1)
    email: str
    password: str
    tickets: List[Ticket] = Field(default_factory=list)

    class Config:
        populate_by_name = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str]
