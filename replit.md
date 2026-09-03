# Irada

## Run the app

The project is a small Flask application. Start it with:

```bash
python app.py
```

The server listens on `0.0.0.0:5000` for the Replit web preview. The `/health`
endpoint returns a JSON status response for a simple runtime check.

## Project status

The current app is an accessible bilingual starter experience. It supports
English and Arabic language switching, updates the document direction for RTL
layouts, and includes translated job discovery content with client-side search
validation. The hiring workflows and data model still need to be designed and
implemented.