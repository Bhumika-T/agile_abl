# Agile Library Management System

Web-based library management system for the Agile Software Development course.
The application is split into independently owned modules that are developed on
separate Git branches, reviewed through pull requests and merged into one Flask app.

## Modules

| Module | Branch | Owner | Status |
| --- | --- | --- | --- |
| Member Registration | `feature/member-registration` | Bhumika T | In development |
| Book Management | `feature/book-management` | Team member 2 | Planned |
| Issue & Return | `feature/issue-return` | Team member 3 | Planned |

This repository currently contains the shared Flask scaffold. Module code lands
through pull requests against `main`.

## Tech stack

- Python 3.9+ with Flask 3
- Flask-SQLAlchemy (SQLite for local development, MySQL via `DATABASE_URL`)
- Jinja templates and a small hand-written CSS design system

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (bash: source .venv/Scripts/activate)
pip install -r requirements.txt
python run.py
```

The app starts at http://127.0.0.1:5000 with a local SQLite database (`library.db`).

## Git workflow

```bash
git switch main
git pull origin main
git switch -c feature/<module-name>
# ... commits for the module ...
git push -u origin feature/<module-name>
```

Open a pull request on the remote, get a teammate review, then merge into `main`.
