"""Core Domain Models (DTOs) for School Hub.

These are Reflex State DTOs designed for in-memory storage and UI rendering.
All display values are strings "as is" from scraped HTML.
Hidden sort_key fields enable cross-provider sorting.
"""

from pydantic import BaseModel
from typing import Optional


class GradeDTO(BaseModel):
    """Represents a single grade or a retake. Denormalized for easy dashboard rendering."""
    
    # --- CONTEXT (Denormalized relations for the Unified Dashboard) ---
    kid_name: str
    subject_name: str

    # --- DISPLAY FIELDS (Strings "As Is" for the UI) ---
    value: str
    category: str
    weight: str
    date: Optional[str] = None
    comment: Optional[str] = None
    
    # --- SORTING FIELDS (Hidden from UI, used only for logic) ---
    # Scrapers must convert Provider-specific date strings into a standard integer (YYYYMMDD)
    date_sort_key: int = 0
    
    # --- RETAKE SPECIFIC FIELDS ---
    is_retake: bool = False
    previous_value: Optional[str] = None
    original_date: Optional[str] = None
    retake_date: Optional[str] = None


class PeriodDTO(BaseModel):
    """Represents a grading period (e.g., 'OKRES 1')."""

    name: str
    grades: list[GradeDTO]
    empty_message: Optional[str] = None


class SubjectDTO(BaseModel):
    """Represents a school subject with its grading periods."""

    name: str
    periods: list[PeriodDTO]


class NewsDTO(BaseModel):
    """Represents a school announcement/message. Denormalized for dashboard."""

    kid_name: str
    date: str
    date_sort_key: int = 0  # e.g., 202510011430 (YYYYMMDDHHMM)
    sender: str
    subject: str
    content: str


class CalendarEventDTO(BaseModel):
    """Represents a calendar event (test, quiz, homework). Denormalized for dashboard."""

    kid_name: str
    date_sort_key: int  # For grouping by day (YYYYMMDD)
    display_date: str  # e.g., "Today, March 6"
    time_range: str  # e.g., "09:50 - 10:35"
    room: str  # e.g., "Room A104a"
    subject: str  # e.g., "Język angielski"
    event_type: str  # e.g., "Sprawdzian", "Kartkówka"
    description: str  # e.g., "sprawdzian chłopcy dział 5"
    teacher: str  # e.g., "Fidali Natalia"
    color_theme: str  # e.g., "red", "blue", "orange" (mapped from subject)


class KidGradesDTO(BaseModel):
    """The root container for a specific child's scraped data."""

    kid_name: str
    provider: str  # "Librus" or "Vulcan"
    subjects: list[SubjectDTO]
    news: list[NewsDTO]
    last_synced: str  # Timestamp string of the last successful scrape

