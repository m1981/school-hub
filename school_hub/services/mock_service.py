"""Mock Monitoring Service for Sprint 1 - generates dummy data for testing UI."""

from school_hub.models import (
    GradeDTO,
    PeriodDTO,
    SubjectDTO,
    NewsDTO,
    CalendarEventDTO,
    KidGradesDTO,
)


class MockMonitoringService:
    """Generates mock data for Anna, Ben, Clara, and David matching the UI mockups."""

    def get_all_data(self) -> list[KidGradesDTO]:
        """Return mock data for all 4 kids."""
        return [
            self._create_anna_data(),
            self._create_ben_data(),
            self._create_clara_data(),
            self._create_david_data(),
        ]

    def _create_anna_data(self) -> KidGradesDTO:
        """Create mock data for Anna (Librus provider)."""
        return KidGradesDTO(
            kid_name="Anna",
            provider="Librus",
            subjects=[
                SubjectDTO(
                    name="Matematyka",
                    periods=[
                        PeriodDTO(
                            name="OKRES 1",
                            grades=[
                                GradeDTO(
                                    kid_name="Anna",
                                    subject_name="Matematyka",
                                    value="5",
                                    category="kartkówka",
                                    weight="2",
                                    date="2025-09-24 (śr.)",
                                    date_sort_key=20250924,
                                ),
                                GradeDTO(
                                    kid_name="Anna",
                                    subject_name="Matematyka",
                                    value="4+",
                                    category="odpowiedź ustna",
                                    weight="1",
                                    date="2025-09-20 (pt.)",
                                    date_sort_key=20250920,
                                ),
                            ],
                        )
                    ],
                ),
                SubjectDTO(
                    name="Język polski",
                    periods=[
                        PeriodDTO(
                            name="OKRES 1",
                            grades=[
                                GradeDTO(
                                    kid_name="Anna",
                                    subject_name="Język polski",
                                    value="6",
                                    category="wypracowanie",
                                    weight="3",
                                    date="2025-09-22 (pon.)",
                                    date_sort_key=20250922,
                                ),
                            ],
                        )
                    ],
                ),
            ],
            news=[
                NewsDTO(
                    kid_name="Anna",
                    date="2025-10-01 14:30",
                    date_sort_key=202510011430,
                    sender="Wychowawca",
                    subject="Zebranie rodziców",
                    content="Zebranie odbędzie się w piątek o 17:00.",
                ),
                NewsDTO(
                    kid_name="Anna",
                    date="2025-09-25 10:15",
                    date_sort_key=202509251015,
                    sender="Dyrektor",
                    subject="Komunikat",
                    content="W przyszłym tygodniu planowane są zawody sportowe.",
                ),
            ],
            calendar_events=[
                CalendarEventDTO(
                    kid_name="Anna",
                    date_sort_key=20260328,
                    display_date="Today, March 28",
                    time_range="09:50 - 10:35",
                    room="Room A104a",
                    subject="Matematyka",
                    event_type="Sprawdzian",
                    description="Sprawdzian z geometrii",
                    teacher="Kowalska Anna",
                    color_theme="blue",
                ),
                CalendarEventDTO(
                    kid_name="Anna",
                    date_sort_key=20260330,
                    display_date="Monday, March 30",
                    time_range="11:00 - 11:45",
                    room="Room B201",
                    subject="Język polski",
                    event_type="Kartkówka",
                    description="Kartkówka z lektury",
                    teacher="Nowak Maria",
                    color_theme="green",
                ),
            ],
            last_synced="2025-10-02 08:30",
        )

    def _create_ben_data(self) -> KidGradesDTO:
        """Create mock data for Ben (Vulcan provider)."""
        return KidGradesDTO(
            kid_name="Ben",
            provider="Vulcan",
            subjects=[
                SubjectDTO(
                    name="Fizyka",
                    periods=[
                        PeriodDTO(
                            name="Semestr 1",
                            grades=[
                                GradeDTO(
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
                                ),
                                GradeDTO(
                                    kid_name="Ben",
                                    subject_name="Fizyka",
                                    value="3+",
                                    category="sprawdzian",
                                    weight="2",
                                    date="2025-11-15 (śr.)",
                                    date_sort_key=20251115,
                                ),
                            ],
                        )
                    ],
                ),
            ],
            news=[
                NewsDTO(
                    kid_name="Ben",
                    date="2025-11-20 09:00",
                    date_sort_key=202511200900,
                    sender="Nauczyciel fizyki",
                    subject="Egzamin",
                    content="Egzamin poprawkowy z fizyki w przyszłym tygodniu.",
                ),
            ],
            calendar_events=[
                CalendarEventDTO(
                    kid_name="Ben",
                    date_sort_key=20260329,
                    display_date="Tomorrow, March 29",
                    time_range="10:00 - 10:45",
                    room="Lab 301",
                    subject="Fizyka",
                    event_type="Kartkówka",
                    description="Kartkówka z optyki",
                    teacher="Wiśniewski Jan",
                    color_theme="red",
                ),
                CalendarEventDTO(
                    kid_name="Ben",
                    date_sort_key=20260401,
                    display_date="Tuesday, April 1",
                    time_range="13:00 - 13:45",
                    room="Lab 301",
                    subject="Fizyka",
                    event_type="Zadania",
                    description="Zadania domowe - mechanika",
                    teacher="Wiśniewski Jan",
                    color_theme="red",
                ),
            ],
            last_synced="2025-11-25 10:00",
        )

    def _create_clara_data(self) -> KidGradesDTO:
        """Create mock data for Clara (Librus provider)."""
        return KidGradesDTO(
            kid_name="Clara",
            provider="Librus",
            subjects=[
                SubjectDTO(
                    name="Historia",
                    periods=[
                        PeriodDTO(
                            name="OKRES 1",
                            grades=[
                                GradeDTO(
                                    kid_name="Clara",
                                    subject_name="Historia",
                                    value="4",
                                    category="karty pracy (S)",
                                    weight="3",
                                    date="2025-12-01 (niedz.)",
                                    date_sort_key=20251201,
                                    comment="Historia - nauka o przeszłości",
                                ),
                                GradeDTO(
                                    kid_name="Clara",
                                    subject_name="Historia",
                                    value="5-",
                                    category="sprawdzian",
                                    weight="3",
                                    date="2025-11-28 (czw.)",
                                    date_sort_key=20251128,
                                ),
                            ],
                        )
                    ],
                ),
            ],
            news=[
                NewsDTO(
                    kid_name="Clara",
                    date="2025-12-02 11:30",
                    date_sort_key=202512021130,
                    sender="Wychowawca",
                    subject="Wycieczka",
                    content="Wycieczka do muzeum w przyszłym miesiącu.",
                ),
            ],
            calendar_events=[
                CalendarEventDTO(
                    kid_name="Clara",
                    date_sort_key=20260328,
                    display_date="Today, March 28",
                    time_range="14:00 - 14:45",
                    room="Room C105",
                    subject="Historia",
                    event_type="Sprawdzian",
                    description="Sprawdzian z II wojny światowej",
                    teacher="Lewandowska Ewa",
                    color_theme="orange",
                ),
            ],
            last_synced="2025-12-03 07:45",
        )

    def _create_david_data(self) -> KidGradesDTO:
        """Create mock data for David (Vulcan provider)."""
        return KidGradesDTO(
            kid_name="David",
            provider="Vulcan",
            subjects=[
                SubjectDTO(
                    name="Język angielski",
                    periods=[
                        PeriodDTO(
                            name="Semestr 1",
                            grades=[
                                GradeDTO(
                                    kid_name="David",
                                    subject_name="Język angielski",
                                    value="5+",
                                    category="sprawdzian",
                                    weight="2",
                                    date="2026-03-05 (czw.)",
                                    date_sort_key=20260305,
                                ),
                                GradeDTO(
                                    kid_name="David",
                                    subject_name="Język angielski",
                                    value="6",
                                    category="odpowiedź ustna",
                                    weight="1",
                                    date="2026-03-01 (niedz.)",
                                    date_sort_key=20260301,
                                ),
                            ],
                        )
                    ],
                ),
            ],
            news=[
                NewsDTO(
                    kid_name="David",
                    date="2026-03-06 08:00",
                    date_sort_key=202603060800,
                    sender="Nauczyciel j. angielskiego",
                    subject="Sprawdzian",
                    content="Sprawdzian z działu 5 w najbliższy piątek.",
                ),
            ],
            calendar_events=[
                CalendarEventDTO(
                    kid_name="David",
                    date_sort_key=20260402,
                    display_date="Wednesday, April 2",
                    time_range="08:00 - 08:45",
                    room="Room D202",
                    subject="Język angielski",
                    event_type="Sprawdzian",
                    description="Sprawdzian chłopcy dział 5",
                    teacher="Fidali Natalia",
                    color_theme="purple",
                ),
                CalendarEventDTO(
                    kid_name="David",
                    date_sort_key=20260405,
                    display_date="Saturday, April 5",
                    time_range="12:00 - 12:45",
                    room="Room D202",
                    subject="Język angielski",
                    event_type="Zadania",
                    description="Zadania - ćwiczenia gramatyczne",
                    teacher="Fidali Natalia",
                    color_theme="purple",
                ),
            ],
            last_synced="2026-03-06 09:00",
        )
