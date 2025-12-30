"""Pydantic schemas for API payloads."""

from datetime import date
from typing import Optional, List
from pydantic import BaseModel


class ScientistCreate(BaseModel):
    full_name: str
    country: Optional[str]
    degree: Optional[str]
    specialization: Optional[str]
    organization: Optional[str]
    extra_data: Optional[dict]


class ScientistRead(ScientistCreate):
    id: int

    class Config:
        from_attributes = True


class ConferenceCreate(BaseModel):
    name: str
    theme: Optional[str]
    topic: Optional[str]
    date: Optional[date]
    place: Optional[str]
    country: Optional[str]
    extra_data: Optional[dict]


class ConferenceRead(ConferenceCreate):
    id: int

    class Config:
        from_attributes = True


class ParticipationCreate(BaseModel):
    scientist_id: int
    conference_id: int
    participation_type: Optional[str]
    topic: Optional[str]
    duration_minutes: Optional[int]
    notes: Optional[str]
    extra_data: Optional[dict]


class ParticipationRead(ParticipationCreate):
    id: int

    class Config:
        from_attributes = True
