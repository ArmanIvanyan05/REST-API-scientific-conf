"""SQLAlchemy models for the Scientific Conferences domain."""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Enum,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Scientist(Base):
    __tablename__ = "scientists"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False, index=True)
    country = Column(String(100), nullable=True)
    degree = Column(String(100), nullable=True)
    specialization = Column(String(255), nullable=True)
    organization = Column(String(255), nullable=True)
    extra_data = Column(JSONB, nullable=True)

    participations = relationship(
        "Participation", back_populates="scientist", cascade="all, delete-orphan"
    )


class Conference(Base):
    __tablename__ = "conferences"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    theme = Column(String(255), nullable=True)
    topic = Column(String(255), nullable=True)
    date = Column(Date, nullable=True)
    place = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    extra_data = Column(JSONB, nullable=True)

    participations = relationship(
        "Participation", back_populates="conference", cascade="all, delete-orphan"
    )


class Participation(Base):
    __tablename__ = "participations"

    id = Column(Integer, primary_key=True)
    scientist_id = Column(
        Integer,
        ForeignKey("scientists.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    conference_id = Column(
        Integer,
        ForeignKey("conferences.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    participation_type = Column(String(100), nullable=True)  # e.g., speaker, attendee
    topic = Column(String(255), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    extra_data = Column(JSONB, nullable=True)

    scientist = relationship("Scientist", back_populates="participations")
    conference = relationship("Conference", back_populates="participations")
