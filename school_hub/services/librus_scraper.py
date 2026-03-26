"""Librus Scraper - Parses Librus HTML into KidGradesDTO.

Based on the POC parser that successfully handles:
- Grade extraction from table rows
- Metadata parsing from title attributes
- Retake (poprawa) merging logic
- Two-period structure (OKRES 1, OKRES 2)
"""

from bs4 import BeautifulSoup
import html
import re
from datetime import datetime
from school_hub.models import (
    GradeDTO,
    PeriodDTO,
    SubjectDTO,
    KidGradesDTO,
)


class LibrusScraper:
    """Scraper for Librus electronic grade book."""

    def parse_grades(self, html_content: str, kid_name: str) -> KidGradesDTO:
        """Parse Librus HTML and return structured grade data.

        Args:
            html_content: Raw HTML from Librus grades page
            kid_name: Name of the student (for denormalization)

        Returns:
            KidGradesDTO with all subjects, periods, and grades
        """
        soup = BeautifulSoup(html_content, "html.parser")
        subjects = []

        # Find all table rows with grades (line0 and line1 classes)
        rows = soup.find_all("tr", class_=["line0", "line1"])

        for row in rows:
            cols = row.find_all("td", recursive=False)
            if len(cols) < 10:
                continue

            # Extract subject name from column 1
            subject_name = cols[1].get_text(strip=True)
            if not subject_name or "Zachowanie" in subject_name:
                continue

            # Extract grades for both periods
            # Column 2 = OKRES 1 grades, Column 6 = OKRES 2 grades
            okres1_grades = self._extract_grades(cols[2], kid_name, subject_name)
            okres2_grades = self._extract_grades(cols[6], kid_name, subject_name)

            # Only add subject if it has at least one grade
            if okres1_grades or okres2_grades:
                subjects.append(
                    SubjectDTO(
                        name=subject_name,
                        periods=[
                            PeriodDTO(
                                name="OKRES 1",
                                grades=okres1_grades,
                                empty_message="Brak ocen"
                                if not okres1_grades
                                else None,
                            ),
                            PeriodDTO(
                                name="OKRES 2",
                                grades=okres2_grades,
                                empty_message="Brak ocen"
                                if not okres2_grades
                                else None,
                            ),
                        ],
                    )
                )

        # Generate timestamp for last_synced
        last_synced = datetime.now().strftime("%Y-%m-%d %H:%M")

        return KidGradesDTO(
            kid_name=kid_name,
            provider="Librus",
            subjects=subjects,
            news=[],  # News parsing not implemented yet
            calendar_events=[],  # Calendar parsing not implemented yet
            last_synced=last_synced,
        )

    def _extract_grades(
        self, td_cell, kid_name: str, subject_name: str
    ) -> list[GradeDTO]:
        """Extract all grades from a table cell.

        This implements the complex logic from the POC:
        - Parse grade metadata from title attributes
        - Merge retake grades with their originals
        - Convert dates to sort keys

        Args:
            td_cell: BeautifulSoup td element containing grades
            kid_name: Student name for denormalization
            subject_name: Subject name for denormalization

        Returns:
            List of GradeDTO objects
        """
        grades = []
        grade_links = td_cell.find_all("a", class_="ocena")

        for link in grade_links:
            ocena_wartosc = link.get_text(strip=True)
            title_content = link.get("title", "")

            if not ocena_wartosc or not title_content:
                continue

            # Decode HTML entities and clean up
            decoded_title = html.unescape(title_content)
            clean_title = re.sub(r"<br\s*/?>", "\n", decoded_title)

            # Parse metadata from title
            details = {}
            for line in clean_title.split("\n"):
                line = line.strip()
                if not line:
                    continue
                if ":" in line:
                    key, val = line.split(":", 1)
                    details[key.strip().lower()] = val.strip()

            # CRITICAL: Retake merging logic from POC
            if "poprawa oceny" in details and len(grades) > 0:
                # This is a retake - merge with the previous grade
                ocena_pierwotna = grades.pop()

                # Create merged retake object
                combined_grade = GradeDTO(
                    kid_name=kid_name,
                    subject_name=subject_name,
                    value=ocena_wartosc,
                    category=details.get("kategoria", ocena_pierwotna.category),
                    weight=details.get("waga", ocena_pierwotna.weight),
                    date=details.get("data"),
                    comment=details.get("komentarz"),
                    date_sort_key=self._parse_date_to_sort_key(details.get("data", "")),
                    is_retake=True,
                    previous_value=ocena_pierwotna.value,
                    original_date=ocena_pierwotna.date,
                    retake_date=details.get("data"),
                )
                grades.append(combined_grade)
            else:
                # Normal grade
                grade = GradeDTO(
                    kid_name=kid_name,
                    subject_name=subject_name,
                    value=ocena_wartosc,
                    category=details.get("kategoria", ""),
                    weight=details.get("waga", ""),
                    date=details.get("data"),
                    comment=details.get("komentarz"),
                    date_sort_key=self._parse_date_to_sort_key(details.get("data", "")),
                    is_retake=False,
                )
                grades.append(grade)

        return grades

    def _parse_date_to_sort_key(self, date_str: str) -> int:
        """Convert Librus date string to YYYYMMDD integer for sorting.

        Librus dates are in format: "2025-01-15 (śr.)" or similar.

        Args:
            date_str: Date string from Librus

        Returns:
            Integer in YYYYMMDD format, or 0 if parsing fails
        """
        if not date_str:
            return 0

        try:
            # Extract just the date part (before the day name in parentheses)
            date_part = date_str.split("(")[0].strip()

            # Try to parse YYYY-MM-DD format
            if "-" in date_part:
                parts = date_part.split("-")
                if len(parts) == 3:
                    year = int(parts[0])
                    month = int(parts[1])
                    day = int(parts[2])
                    return year * 10000 + month * 100 + day

            # Try to parse DD.MM.YYYY format
            if "." in date_part:
                parts = date_part.split(".")
                if len(parts) == 3:
                    day = int(parts[0])
                    month = int(parts[1])
                    year = int(parts[2])
                    return year * 10000 + month * 100 + day

        except (ValueError, IndexError):
            pass

        return 0
