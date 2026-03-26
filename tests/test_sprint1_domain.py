"""Sprint 1 Tests: Core Domain & Mock Data.
TDD Red phase – these tests define expected behaviour before implementation.
"""

import pytest
from school_hub.models import (
    GradeDTO,
    PeriodDTO,
    SubjectDTO,
    NewsDTO,
    KidGradesDTO,
    CalendarEventDTO,
)
from school_hub.services.mock_service import MockMonitoringService

# ---------------------------------------------------------------------------
# DTO structure tests
# ---------------------------------------------------------------------------


def test_grade_dto_defaults_are_correct():
    """GradeDTO should have sensible defaults for optional fields."""
    # Given / When
    grade = GradeDTO(
        kid_name="Anna",
        subject_name="Matematyka",
        value="5",
        category="kartkówka",
        weight="2",
    )
    # Then
    assert grade.is_retake is False
    assert grade.date_sort_key == 0
    assert grade.previous_value is None
    assert grade.original_date is None
    assert grade.retake_date is None


def test_grade_dto_retake_fields_populated():
    """GradeDTO should store retake-specific fields when is_retake=True."""
    # Given / When
    grade = GradeDTO(
        kid_name="Ben",
        subject_name="Fizyka",
        value="4",
        category="poprawa",
        weight="1",
        is_retake=True,
        previous_value="2",
        original_date="2025-11-10 (pon.)",
        retake_date="2025-11-24 (pon.)",
        date_sort_key=20251124,
    )
    # Then
    assert grade.is_retake is True
    assert grade.previous_value == "2"
    assert grade.retake_date == "2025-11-24 (pon.)"


def test_news_dto_has_required_fields():
    """NewsDTO should store all denormalized fields."""
    # Given / When
    news = NewsDTO(
        kid_name="Clara",
        date="2025-10-01 14:30",
        date_sort_key=202510011430,
        sender="Wychowawca",
        subject="Zebranie rodziców",
        content="Zebranie odbędzie się w piątek.",
    )
    # Then
    assert news.kid_name == "Clara"
    assert news.date_sort_key == 202510011430


def test_calendar_event_dto_has_color_theme():
    """CalendarEventDTO should carry a color_theme field."""
    # Given / When
    event = CalendarEventDTO(
        kid_name="David",
        date_sort_key=20260306,
        display_date="Today, March 6",
        time_range="09:50 - 10:35",
        room="Room A104a",
        subject="Język angielski",
        event_type="Sprawdzian",
        description="sprawdzian dział 5",
        teacher="Fidali Natalia",
        color_theme="blue",
    )
    # Then
    assert event.color_theme == "blue"
    assert event.event_type == "Sprawdzian"


def test_kid_grades_dto_contains_subjects_and_news():
    """KidGradesDTO should aggregate subjects and news lists."""
    # Given / When
    kid = KidGradesDTO(
        kid_name="Anna",
        provider="Librus",
        subjects=[],
        news=[],
        last_synced="2025-01-01 00:00",
    )
    # Then
    assert kid.provider == "Librus"
    assert isinstance(kid.subjects, list)
    assert isinstance(kid.news, list)


# ---------------------------------------------------------------------------
# MockMonitoringService tests
# ---------------------------------------------------------------------------


def test_mock_service_returns_four_kids():
    """MockMonitoringService.get_all_data() must return exactly 4 KidGradesDTOs."""
    # Given
    service = MockMonitoringService()
    # When
    result = service.get_all_data()
    # Then
    assert len(result) == 4


def test_mock_service_kid_names():
    """MockMonitoringService should return data for Anna, Ben, Clara, and David."""
    # Given
    service = MockMonitoringService()
    # When
    result = service.get_all_data()
    names = {kid.kid_name for kid in result}
    # Then
    assert names == {"Anna", "Ben", "Clara", "David"}


def test_mock_service_each_kid_has_at_least_one_subject():
    """Each KidGradesDTO from mock service must have at least one subject."""
    # Given
    service = MockMonitoringService()
    # When
    result = service.get_all_data()
    # Then
    for kid in result:
        assert len(kid.subjects) >= 1, f"{kid.kid_name} has no subjects"


def test_mock_service_each_kid_has_at_least_one_news():
    """Each KidGradesDTO from mock service must have at least one news item."""
    # Given
    service = MockMonitoringService()
    # When
    result = service.get_all_data()
    # Then
    for kid in result:
        assert len(kid.news) >= 1, f"{kid.kid_name} has no news"


def test_mock_service_grades_have_valid_date_sort_keys():
    """All grades returned by mock service must have non-zero date_sort_key."""
    # Given
    service = MockMonitoringService()
    # When
    result = service.get_all_data()
    # Then
    for kid in result:
        for subject in kid.subjects:
            for period in subject.periods:
                for grade in period.grades:
                    assert grade.date_sort_key > 0, (
                        f"Grade {grade.value} for {grade.kid_name} / "
                        f"{grade.subject_name} has date_sort_key=0"
                    )


def test_mock_service_grades_are_denormalized():
    """All grades must carry kid_name and subject_name (denormalization check)."""
    # Given
    service = MockMonitoringService()
    # When
    result = service.get_all_data()
    # Then
    for kid in result:
        for subject in kid.subjects:
            for period in subject.periods:
                for grade in period.grades:
                    assert grade.kid_name != "", "kid_name must not be empty"
                    assert grade.subject_name != "", "subject_name must not be empty"


def test_mock_service_news_sort_keys_are_nonzero():
    """All news items from mock service must have non-zero date_sort_key."""
    # Given
    service = MockMonitoringService()
    # When
    result = service.get_all_data()
    # Then
    for kid in result:
        for news in kid.news:
            assert news.date_sort_key > 0, (
                f"News '{news.subject}' for {news.kid_name} has date_sort_key=0"
            )

