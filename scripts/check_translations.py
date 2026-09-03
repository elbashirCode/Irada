"""Validate the bilingual translation contract embedded in app.py."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "app.py"


def _extract_catalogs(page: str) -> dict[str, dict[str, str]]:
    """Extract the simple English and Arabic catalogs from the page script."""
    catalogs_match = re.search(
        r"\btranslations\s*=\s*\{\s*"
        r"en:\s*\{(?P<en>.*?)\n\s*\},\s*"
        r"ar:\s*\{(?P<ar>.*?)\n\s*\}\s*\};",
        page,
        re.DOTALL,
    )
    if not catalogs_match:
        raise ValueError("Could not find both translation catalogs in app.py")

    catalogs: dict[str, dict[str, str]] = {}
    entry_pattern = re.compile(
        r'^\s*(?P<key>[A-Za-z][A-Za-z0-9_]*):\s*"(?P<value>(?:\\.|[^"\\])*)",?\s*$',
        re.MULTILINE,
    )
    for language in ("en", "ar"):
        entries = {
            match.group("key"): json.loads(f'"{match.group("value")}"')
            for match in entry_pattern.finditer(catalogs_match.group(language))
        }
        if not entries:
            raise ValueError(f"The {language} translation catalog is empty")
        catalogs[language] = entries
    return catalogs


def _extract_referenced_keys(page: str) -> tuple[set[str], set[str]]:
    """Find UI keys and job catalog keys used by the rendered page."""
    ui_keys = set(
        re.findall(r'data-i18n(?:-[A-Za-z0-9-]+)?="([^"]+)"', page)
    )
    ui_keys.update(re.findall(r'\btext\("([^"]+)"\)', page))
    ui_keys.update(re.findall(r'\bshowSearchMessage\("([^"]+)"', page))
    ui_keys.update({"pageTitle", "pageDescription"})

    jobs_match = re.search(
        r"const jobs\s*=\s*\[(?P<jobs>.*?)\n\s*\];",
        page,
        re.DOTALL,
    )
    if not jobs_match:
        raise ValueError("Could not find the jobs catalog in app.py")
    job_keys = set(
        re.findall(
            r'\b(?:title|company|description|typeLabel):\s*"([^"]+)"',
            jobs_match.group("jobs"),
        )
    )
    ui_keys.discard("job-list")
    return ui_keys, job_keys


def _extract_jobs(page: str) -> list[dict[str, str]]:
    """Extract the small job catalog used by the page's client-side search."""
    jobs_match = re.search(
        r"const jobs\s*=\s*\[(?P<jobs>.*?)\n\s*\];",
        page,
        re.DOTALL,
    )
    if not jobs_match:
        raise ValueError("Could not find the jobs catalog in app.py")

    return [
        dict(re.findall(r'\b([A-Za-z][A-Za-z0-9_]*):\s*"([^"]+)"', job))
        for job in re.findall(r"\{([^{}]+)\}", jobs_match.group("jobs"))
    ]


class _SearchMarkupParser(HTMLParser):
    """Capture the browser-facing elements needed to submit a search."""

    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del tag
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            self.ids.add(element_id)


def _check_search_flow(page: str) -> list[str]:
    """Exercise the browser-facing search contract for both supported languages."""
    try:
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        from app import app

        with app.test_client() as client:
            response = client.get("/")
    except Exception as error:
        return [f"Could not load the search page: {error}"]

    if response.status_code != 200:
        return [f"Search page returned HTTP {response.status_code}"]

    rendered_page = response.get_data(as_text=True)
    parser = _SearchMarkupParser()
    parser.feed(rendered_page)
    required_ids = {"job-search", "keyword", "work-type", "search-message", "job-list"}
    missing_ids = sorted(required_ids - parser.ids)
    errors: list[str] = []
    if missing_ids:
        errors.append(
            "Search page is missing browser element(s): " + ", ".join(missing_ids)
        )

    # Keep this check tied to the actual branch in the page script. The cases
    # below then verify that each branch renders the selected catalog message.
    branch_pattern = (
        r'const resultMessageKey = filteredJobs\.length === 0\s*'
        r'\?\s*"searchNone"\s*'
        r': filteredJobs\.length === 1\s*'
        r'\?\s*"searchFoundOne"\s*'
        r':\s*"searchFoundMany"'
    )
    if not re.search(branch_pattern, rendered_page):
        errors.append(
            "Search flow must select searchNone, searchFoundOne, or "
            "searchFoundMany by result count"
        )

    catalogs = _extract_catalogs(rendered_page)
    jobs = _extract_jobs(rendered_page)
    scenarios = (
        ("ar", "ال", 3, "وجدنا 3 وظائف تطابق بحثك عن «ال»."),
        ("ar", "دعم", 1, "وجدنا وظيفة واحدة تطابق بحثك عن «دعم»."),
        (
            "ar",
            "زقزوق",
            0,
            "لا توجد وظائف تطابق بحثك عن «زقزوق» حالياً. جرّب بحثاً آخر.",
        ),
        ("en", "support", 1, "1 roles match “support”."),
    )
    for language, keyword, expected_count, expected_message in scenarios:
        matches = [
            job
            for job in jobs
            if keyword.casefold()
            in " ".join(
                catalogs[search_language][job[field]]
                for search_language in ("en", "ar")
                for field in ("title", "company", "description")
            ).casefold()
        ]
        count = len(matches)
        result_key = (
            "searchNone"
            if count == 0
            else "searchFoundOne"
            if count == 1
            else "searchFoundMany"
        )
        message = catalogs[language][result_key]
        message = message.replace("{count}", str(count)).replace("{keyword}", keyword)
        label = f"{language} search for {keyword!r}"
        if count != expected_count:
            errors.append(
                f"{label} expected {expected_count} result(s), found {count}"
            )
        if message != expected_message:
            errors.append(
                f"{label} rendered unexpected message: {message!r}"
            )
        if keyword not in message:
            errors.append(f"{label} omitted the searched keyword")
        if "{count}" in message or "{keyword}" in message:
            errors.append(f"{label} left an interpolation placeholder unresolved")

    return errors


def validate(page: str) -> list[str]:
    """Return all translation contract violations found in the page."""
    catalogs = _extract_catalogs(page)
    ui_keys, job_keys = _extract_referenced_keys(page)
    referenced_keys = ui_keys | job_keys
    errors: list[str] = []

    english_keys = set(catalogs["en"])
    arabic_keys = set(catalogs["ar"])
    for language, keys in (("English", english_keys), ("Arabic", arabic_keys)):
        missing = sorted(referenced_keys - keys)
        if missing:
            errors.append(
                f"{language} is missing referenced key(s): {', '.join(missing)}"
            )

    only_english = sorted(english_keys - arabic_keys)
    if only_english:
        errors.append(
            "Arabic is missing catalog key(s): " + ", ".join(only_english)
        )
    only_arabic = sorted(arabic_keys - english_keys)
    if only_arabic:
        errors.append(
            "English is missing catalog key(s): " + ", ".join(only_arabic)
        )

    for key in sorted(referenced_keys & english_keys & arabic_keys):
        english_value = catalogs["en"][key].strip()
        arabic_value = catalogs["ar"][key].strip()
        if not english_value:
            errors.append(f"English translation is empty for key: {key}")
        if not arabic_value:
            errors.append(f"Arabic translation is empty for key: {key}")
        if arabic_value == english_value:
            errors.append(
                f"Arabic translation unexpectedly matches English for key: {key}"
            )

    return errors


def main() -> int:
    try:
        page = APP_PATH.read_text(encoding="utf-8")
        errors = validate(page)
        errors.extend(_check_search_flow(page))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Translation check failed: {error}", file=sys.stderr)
        return 1

    if errors:
        print("Translation check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    catalogs = _extract_catalogs(APP_PATH.read_text(encoding="utf-8"))
    ui_keys, job_keys = _extract_referenced_keys(
        APP_PATH.read_text(encoding="utf-8")
    )
    print(
        "Translation check passed: "
        f"{len(ui_keys)} UI keys and {len(job_keys)} job keys "
        "have English and Arabic values."
    )
    print("Search flow check passed: Arabic zero/one/many and English baseline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())