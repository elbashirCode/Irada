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