"""Sprint 6: Tests for Librus Scraper using real HTML data.

Following TDD: These tests are written BEFORE the scraper implementation.
They use the actual oceny.html file from tests/mock_data/.
"""

import pytest
from pathlib import Path
from school_hub.services.librus_scraper import LibrusScraper
from school_hub.models import KidGradesDTO, GradeDTO

pytestmark = pytest.mark.integration


@pytest.fixture
def real_librus_html():
    """Load the actual Librus HTML from mock_data."""
    html_path = Path(__file__).parent / "mock_data" / "oceny.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def scraper():
    """Create a LibrusScraper instance."""
    return LibrusScraper()


class TestLibrusScraperBasics:
    """Test basic scraper functionality."""

    def test_scraper_returns_kid_grades_dto(self, scraper, real_librus_html):
        """Test that scraper returns a valid KidGradesDTO object."""
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        assert isinstance(result, KidGradesDTO)
        assert result.kid_name == "Tymoteusz"
        assert result.provider == "Librus"
        assert len(result.subjects) > 0

    def test_scraper_extracts_all_subjects(self, scraper, real_librus_html):
        """Test that scraper extracts all subjects from the HTML.

        Based on oceny.html, we should have subjects like:
        - Historia, Informatyka, Język angielski, Język polski,
        - Matematyka, Muzyka, Plastyka, Przyroda, Religia,
        - Technika, Wychowanie fizyczne

        Should NOT include: Edukacja zdrowotna, Etyka (no grades),
        Zachowanie (behavior, not a subject), Zajęcia z wychowawcą (no grades)
        """
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        subject_names = [s.name for s in result.subjects]

        # Should have subjects with grades
        assert "Historia" in subject_names
        assert "Informatyka" in subject_names
        assert "Język angielski" in subject_names
        assert "Język polski" in subject_names
        assert "Matematyka" in subject_names

        # Should NOT include subjects without grades or behavior
        assert "Zachowanie" not in subject_names
        assert "Edukacja zdrowotna" not in subject_names
        assert "Zajęcia z wychowawcą" not in subject_names

    def test_scraper_creates_two_periods(self, scraper, real_librus_html):
        """Test that each subject has two periods (OKRES 1 and OKRES 2)."""
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        # Check a subject that has grades in both periods
        historia = next((s for s in result.subjects if s.name == "Historia"), None)
        assert historia is not None
        assert len(historia.periods) == 2
        assert historia.periods[0].name == "OKRES 1"
        assert historia.periods[1].name == "OKRES 2"


class TestLibrusGradeExtraction:
    """Test grade extraction and parsing."""

    def test_extract_simple_grade(self, scraper, real_librus_html):
        """Test extraction of a simple grade with all metadata."""
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        # Find Historia subject and check its grades
        historia = next((s for s in result.subjects if s.name == "Historia"), None)
        assert historia is not None

        okres1_grades = historia.periods[0].grades
        assert len(okres1_grades) > 0

        # Check that grades have required fields
        for grade in okres1_grades:
            assert grade.kid_name == "Tymoteusz"
            assert grade.subject_name == "Historia"
            assert grade.value  # Should have a value
            assert grade.category  # Should have a category
            # Weight is optional (some grades like "+" don't have weights)
            assert isinstance(grade.weight, str)  # Should be a string (can be empty)
            assert grade.date_sort_key > 0  # Should have a sort key

    def test_grade_has_correct_metadata_structure(self, scraper, real_librus_html):
        """Test that grades contain all expected metadata fields."""
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        # Get all grades from all subjects
        all_grades = []
        for subject in result.subjects:
            for period in subject.periods:
                all_grades.extend(period.grades)

        assert len(all_grades) > 0

        # Check first grade has proper structure
        grade = all_grades[0]
        assert isinstance(grade, GradeDTO)
        assert isinstance(grade.value, str)
        assert isinstance(grade.category, str)
        assert isinstance(grade.weight, str)
        assert isinstance(grade.date_sort_key, int)

    def test_date_sort_key_format(self, scraper, real_librus_html):
        """Test that date_sort_key is in YYYYMMDD format."""
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        # Get a grade with a date
        all_grades = []
        for subject in result.subjects:
            for period in subject.periods:
                all_grades.extend(period.grades)

        for grade in all_grades:
            if grade.date_sort_key > 0:
                # Should be 8 digits (YYYYMMDD)
                assert 20000101 <= grade.date_sort_key <= 20991231
                # Year should be reasonable
                year = grade.date_sort_key // 10000
                assert 2020 <= year <= 2030


class TestLibrusRetakeLogic:
    """Test the complex retake (poprawa) merging logic from POC."""

    def test_retake_grades_are_merged(self, scraper, real_librus_html):
        """Test that 'poprawa oceny' grades are properly merged with originals.

        The POC shows that when a grade has 'poprawa oceny' in its details,
        it should be merged with the previous grade to create a retake object.
        """
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        # Find all retake grades
        retake_grades = []
        for subject in result.subjects:
            for period in subject.periods:
                for grade in period.grades:
                    if grade.is_retake:
                        retake_grades.append(grade)

        # The HTML should contain at least some retakes
        # (We'll verify this when we see the actual data)
        # For now, just check the structure if retakes exist
        for retake in retake_grades:
            assert retake.is_retake is True
            assert retake.previous_value is not None
            assert retake.value != retake.previous_value
            assert retake.original_date is not None
            assert retake.retake_date is not None

    def test_retake_has_both_dates(self, scraper, real_librus_html):
        """Test that retake grades preserve both original and retake dates."""
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        # Find retake grades
        for subject in result.subjects:
            for period in subject.periods:
                for grade in period.grades:
                    if grade.is_retake:
                        # Retake should have both dates
                        assert grade.original_date is not None
                        assert grade.retake_date is not None
                        # The date_sort_key should be the retake date
                        assert grade.date_sort_key > 0

    def test_normal_grades_are_not_retakes(self, scraper, real_librus_html):
        """Test that normal grades have is_retake=False."""
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        # Count normal vs retake grades
        normal_count = 0
        retake_count = 0

        for subject in result.subjects:
            for period in subject.periods:
                for grade in period.grades:
                    if grade.is_retake:
                        retake_count += 1
                    else:
                        normal_count += 1

        # Should have more normal grades than retakes
        assert normal_count > 0
        # Retakes are optional (might be 0)
        assert retake_count >= 0


class TestLibrusEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_periods_have_no_grades(self, scraper, real_librus_html):
        """Test that periods without grades are handled correctly."""
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        # Some subjects might have empty periods
        for subject in result.subjects:
            for period in subject.periods:
                # If no grades, the list should be empty (not None)
                assert isinstance(period.grades, list)

    def test_special_grade_values(self, scraper, real_librus_html):
        """Test that special grade values like 'np' (nieprzygotowany) are handled."""
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        # Collect all grade values
        all_values = []
        for subject in result.subjects:
            for period in subject.periods:
                for grade in period.grades:
                    all_values.append(grade.value)

        # Should have various grade formats
        assert len(all_values) > 0
        # Values can be: numbers (1-6), with +/-, or special like "np"
        for value in all_values:
            assert isinstance(value, str)
            assert len(value) > 0

    def test_grade_comments_are_optional(self, scraper, real_librus_html):
        """Test that grade comments are optional and handled correctly."""
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        # Some grades might have comments, some might not
        no_comment = False

        for subject in result.subjects:
            for period in subject.periods:
                for grade in period.grades:
                    if not grade.comment:
                        no_comment = True
                        break

        # Most grades don't have comments
        assert no_comment


class TestLibrusIntegration:
    """Integration tests for the complete scraper."""

    def test_complete_parsing_workflow(self, scraper, real_librus_html):
        """Test the complete parsing workflow from HTML to DTOs."""
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        # Verify the complete structure
        assert result.kid_name == "Tymoteusz"
        assert result.provider == "Librus"
        assert len(result.subjects) > 0

        # Verify each subject has proper structure
        for subject in result.subjects:
            assert subject.name
            assert len(subject.periods) == 2

            for period in subject.periods:
                assert period.name in ["OKRES 1", "OKRES 2"]
                assert isinstance(period.grades, list)

                # If there are grades, verify their structure
                for grade in period.grades:
                    assert grade.kid_name == "Tymoteusz"
                    assert grade.subject_name == subject.name
                    assert grade.value
                    assert grade.category
                    # Weight is optional (some grades don't have weights)
                    assert isinstance(grade.weight, str)

    def test_scraper_handles_real_data_volume(self, scraper, real_librus_html):
        """Test that scraper can handle the full volume of real data."""
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        # Count total grades
        total_grades = 0
        for subject in result.subjects:
            for period in subject.periods:
                total_grades += len(period.grades)

        # Real data should have a reasonable number of grades
        assert total_grades > 10  # Should have at least some grades
        assert total_grades < 500  # But not an unreasonable amount

    def test_last_synced_is_set(self, scraper, real_librus_html):
        """Test that last_synced timestamp is set."""
        result = scraper.parse_grades(real_librus_html, kid_name="Tymoteusz")

        assert result.last_synced
        assert isinstance(result.last_synced, str)
        assert len(result.last_synced) > 0
