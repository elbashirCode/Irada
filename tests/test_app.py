import unittest
from html.parser import HTMLParser

from app import app


class _PageMarkupParser(HTMLParser):
    """Collect the page elements needed for the accessibility contract."""

    _VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__()
        self.elements = []
        self._text_stack = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        element = {"tag": tag, "attrs": attributes, "text": ""}
        self.elements.append(element)
        if tag not in self._VOID_TAGS:
            self._text_stack.append(element)

    def handle_startendtag(self, tag, attrs):
        self.elements.append({"tag": tag, "attrs": dict(attrs), "text": ""})

    def handle_data(self, data):
        for element in self._text_stack:
            element["text"] += data

    def handle_endtag(self, tag):
        for index in range(len(self._text_stack) - 1, -1, -1):
            if self._text_stack[index]["tag"] == tag:
                del self._text_stack[index:]
                break


class AppSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.client = app.test_client()

    def test_home_page_is_successful_and_contains_irada_content(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Irada", response.get_data(as_text=True))
        self.assertIn("إرادة", response.get_data(as_text=True))

    def test_health_endpoint_returns_ok_status(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_home_page_preserves_accessible_structure(self):
        response = self.client.get("/")
        page = response.get_data(as_text=True)
        parser = _PageMarkupParser()
        parser.feed(page)

        elements = parser.elements
        mains = [element for element in elements if element["tag"] == "main"]
        self.assertEqual(len(mains), 1)
        self.assertEqual(mains[0]["attrs"].get("id"), "main-content")
        self.assertEqual(mains[0]["attrs"].get("tabindex"), "-1")

        headings = [
            element
            for element in elements
            if element["tag"] in {"h1", "h2", "h3"}
        ]
        h1s = [element for element in headings if element["tag"] == "h1"]
        self.assertEqual(len(h1s), 1)
        self.assertEqual(h1s[0]["attrs"].get("id"), "hero-title")
        heading_levels = [int(heading["tag"][1]) for heading in headings]
        self.assertEqual(heading_levels[0], 1)
        self.assertTrue(
            all(
                level <= previous_level + 1
                for previous_level, level in zip(heading_levels, heading_levels[1:])
            )
        )

        sections = [
            element
            for element in elements
            if element["tag"] == "section" and element["attrs"].get("aria-labelledby")
        ]
        self.assertEqual(
            {section["attrs"]["aria-labelledby"] for section in sections},
            {"hero-title", "jobs-title", "how-title"},
        )
        heading_ids = {heading["attrs"].get("id") for heading in headings}
        self.assertEqual(
            {section["attrs"]["aria-labelledby"] for section in sections} - heading_ids,
            set(),
        )

        forms = [
            element
            for element in elements
            if element["tag"] == "form" and element["attrs"].get("id") == "job-search"
        ]
        self.assertEqual(len(forms), 1)
        self.assertEqual(forms[0]["attrs"].get("aria-labelledby"), "jobs-title")
        search_form_index = elements.index(forms[0])
        form_controls = elements[search_form_index:]
        keyword = next(
            element
            for element in form_controls
            if element["tag"] == "input" and element["attrs"].get("id") == "keyword"
        )
        work_type = next(
            element
            for element in form_controls
            if element["tag"] == "select" and element["attrs"].get("id") == "work-type"
        )
        self.assertEqual(keyword["attrs"].get("type"), "search")
        self.assertEqual(keyword["attrs"].get("aria-describedby"), "search-message")
        self.assertIn("required", keyword["attrs"])
        self.assertEqual(keyword["attrs"].get("minlength"), "2")
        self.assertEqual(work_type["attrs"].get("name"), "workType")
        labels_by_control = {
            element["attrs"].get("for")
            for element in form_controls
            if element["tag"] == "label"
        }
        self.assertEqual(labels_by_control, {"keyword", "work-type"})
        submit_buttons = [
            element
            for element in form_controls
            if element["tag"] == "button" and element["attrs"].get("type") == "submit"
        ]
        self.assertEqual(len(submit_buttons), 1)
        self.assertTrue(submit_buttons[0]["text"].strip())

        search_message = next(
            element
            for element in elements
            if element["attrs"].get("id") == "search-message"
        )
        job_list = next(
            element
            for element in elements
            if element["attrs"].get("id") == "job-list"
        )
        self.assertEqual(search_message["attrs"].get("role"), "status")
        self.assertEqual(search_message["attrs"].get("aria-live"), "polite")
        self.assertEqual(job_list["attrs"].get("aria-live"), "polite")

        skip_link = next(
            element
            for element in elements
            if element["tag"] == "a" and "skip-link" in element["attrs"].get("class", "")
        )
        self.assertEqual(skip_link["attrs"].get("href"), "#main-content")

        language_groups = [
            element
            for element in elements
            if element["attrs"].get("role") == "group"
            and "language-switcher" in element["attrs"].get("class", "")
        ]
        self.assertEqual(len(language_groups), 1)
        self.assertEqual(language_groups[0]["attrs"].get("aria-label"), "Language")
        language_buttons = [
            element
            for element in elements
            if element["tag"] == "button" and element["attrs"].get("data-language")
        ]
        self.assertEqual(
            {button["attrs"]["data-language"] for button in language_buttons},
            {"en", "ar"},
        )
        self.assertTrue(
            all(
                button["attrs"].get("type") == "button"
                and button["attrs"].get("aria-pressed") in {"true", "false"}
                and button["text"].strip()
                for button in language_buttons
            )
        )

        navigation = next(element for element in elements if element["tag"] == "nav")
        self.assertEqual(navigation["attrs"].get("aria-label"), "Primary navigation")
        links = [element for element in elements if element["tag"] == "a"]
        self.assertTrue(
            all(
                link["attrs"].get("href")
                and (link["attrs"].get("aria-label") or link["text"].strip())
                for link in links
            )
        )

    def test_home_page_includes_responsive_and_focus_regression_contract(self):
        response = self.client.get("/")
        page = response.get_data(as_text=True)

        self.assertIn('<meta name="viewport" content="width=device-width, initial-scale=1">', page)
        self.assertIn("@media (max-width: 840px)", page)
        self.assertIn("header { flex-wrap: wrap; row-gap: 14px; }", page)
        self.assertIn("grid-template-columns: minmax(0, 1fr) auto;", page)
        self.assertIn("grid-column: 1 / -1;", page)
        self.assertIn(":focus-visible", page)
        self.assertIn("mainContent.focus({ preventScroll: true })", page)

if __name__ == "__main__":
    unittest.main()