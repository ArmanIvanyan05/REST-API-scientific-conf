# REST API — Scientific Conferences

This repository contains a small REST API for managing scientists, conferences, and participations. It uses FastAPI + SQLAlchemy + Alembic.

Quick start (Windows PowerShell):

```powershell
# create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

# run the app
$env:DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/scientific_conf"
uvicorn src.app.main:app --reload
```

What's included now:

- `requirements.txt` — Python dependencies
- `src/app/` — application package (minimal starter)
- `.gitignore` — recommended ignores

Next steps (I'll implement): database init script, models, Alembic migrations, CRUD endpoints, data-loader, tests, and more.

# REST-API-scientific-conf
