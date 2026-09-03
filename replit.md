# Irada

## Run the app

The project is a small Flask application. Start it with:

```bash
python app.py
```

The server listens on `0.0.0.0:5000` for the Replit web preview. The `/health`
endpoint returns a JSON status response for a simple runtime check.

## Validation

Run the smoke tests with:

```bash
python -m unittest discover -s tests
```

The smoke suite also checks the home page's landmarks, heading hierarchy,
search controls, language controls, and keyboard-relevant labels and
attributes.

### Responsive and keyboard preview check

Use the running Preview to repeat this browser-facing check:

1. Open the home page at a 320px-wide mobile viewport. Confirm the brand,
   language buttons, all navigation links, hero actions, and search controls
   are visible and reachable without horizontal scrolling.
2. Set the browser zoom to 200% with the viewport still at its normal desktop
   width. Confirm the header navigation moves to its own row and the search
   controls remain reachable without horizontal scrolling.
3. Press `Tab` from the page start. Confirm the skip link has a visible focus
   indicator. Activate it and confirm focus moves to the main content before
   continuing through the page controls.
4. Repeat at 320px wide with Arabic selected. Confirm the same checks pass in
   the right-to-left layout.

The responsive breakpoints and skip-link target are also protected by
`test_home_page_includes_responsive_and_focus_regression_contract` in the
smoke suite.

Run the normal validation checks with:

```bash
bash scripts/post-merge.sh
```

This compiles the Flask app and checks that every UI and job translation
reference has a non-empty English and Arabic value. It also rejects Arabic
values that accidentally duplicate their English fallback.

## Project status

The current app is an accessible bilingual starter experience. It supports
English and Arabic language switching, updates the document direction for RTL
layouts, and includes translated job discovery content with client-side search
validation. The hiring workflows and data model still need to be designed and
implemented.