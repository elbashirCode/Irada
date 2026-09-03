"""Validate the bilingual translation contract embedded in app.py."""

from __future__ import annotations

import json
import re
import sys
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
        errors = validate(APP_PATH.read_text(encoding="utf-8"))
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())