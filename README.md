# Agile Library Management System

Web-based **Library Management System** built for the Agile Software Development
course. The application is split into modules that are developed on separate Git
branches, reviewed through pull requests and merged into `main` — this repository
demonstrates that collaborative workflow end to end.

**Remote repository:** https://github.com/Bhumika-T/agile_abl
(The same branch/PR flow applies to a Gitea remote.)

## Modules

| Module | Branch | Owner | Status |
| --- | --- | --- | --- |
| Member Registration | `feature/member-registration` | Bhumika T | Implemented |
| Book Management | `feature/book-management` | Team member 2 | Planned |
| Issue & Return | `feature/issue-return` | Team member 3 | Planned |

All modules share one Flask application factory and mount their work as a blueprint,
so the member, book and lending modules stay independent inside a single deployable app.

## Tech stack

| Layer | Choice |
| --- | --- |
| Backend | Python 3.9+, Flask 3 |
| ORM | Flask-SQLAlchemy 3 (SQLAlchemy 2) |
| Database | SQLite for local development, MySQL 8 for the shared team database |
| Frontend | Jinja2 templates, hand-written responsive CSS |
| Testing | pytest |

## Member registration module

- Register members with server-validated name, email, phone, address and membership type.
- Auto-generated, human-readable membership codes (`MEM-0001`, `MEM-0002`, ...).
- Duplicate emails rejected case-insensitively (validated in the form and by a
  database unique constraint).
- Member directory with keyword search (name / email / code) and Active / Inactive filters.
- Member profile with contact details, join date and a one-click status toggle.
- Edit member details; the membership code never changes.
- Responsive screens verified at tablet (~860 px) and mobile widths, with a
  `prefers-reduced-motion` fallback for animation-sensitive users.
- Refined, accessible interface: gradient accents, hover/focus states, copy-to-clipboard
  membership codes, dismissible flash messages, form submit feedback and a live
  character counter. Entrance/hover motion only runs when `prefers-reduced-motion` allows it.

### Routes

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | Dashboard with member statistics and module overview |
| GET | `/members/` | Member directory with search and status filters |
| GET, POST | `/members/register` | Registration form |
| GET | `/members/<id>` | Member profile |
| GET, POST | `/members/<id>/edit` | Edit member details |
| POST | `/members/<id>/toggle-status` | Activate / deactivate a member |

## Project structure

```
agile_abl/
├── run.py                  # development entry point
├── seed.py                 # sample members for demos
├── requirements.txt
├── app/
│   ├── __init__.py         # application factory, blueprint registration
│   ├── config.py           # SQLite default, MySQL via DATABASE_URL
│   ├── extensions.py       # SQLAlchemy instance
│   ├── models.py           # Member model + membership code generation
│   ├── main/               # dashboard blueprint
│   ├── members/            # member registration blueprint
│   │   ├── routes.py
│   │   └── forms.py        # server-side validation
│   ├── templates/
│   └── static/css/style.css
└── tests/
    └── test_members.py
```

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate              # Windows (bash: source .venv/Scripts/activate)
pip install -r requirements.txt
python run.py
```

The app starts at http://127.0.0.1:5000 with a local SQLite database (`library.db`,
created automatically). Optional sample data:

```bash
python seed.py
```

### Using MySQL

```sql
CREATE DATABASE library_db CHARACTER SET utf8mb4;
```

Then point the app at MySQL before starting it:

```bash
# Windows (bash)
export DATABASE_URL="mysql+pymysql://root:password@localhost/library_db"
python run.py
```

`PyMySQL` is already in `requirements.txt`. Tables are created on first start.

## Run the tests

```bash
.venv\Scripts\python -m pytest -q
```

The suite covers registration, validation errors, duplicate-email handling, code
generation, search/filters, editing, status toggling and 404s.

## Git collaboration workflow

The project follows a branch-per-module workflow with pull-request reviews:

```bash
# One-time: clone and pick up the shared baseline
git clone https://github.com/Bhumika-T/agile_abl.git
cd agile_abl
git switch main

# Each module owner works on a dedicated branch
git switch -c feature/member-registration
# ... small, focused commits ...
git push -u origin feature/member-registration
```

Then on the remote:

1. **Open a pull request** from the feature branch into `main`.
2. **Review the diff**: check naming, validation, tests and that `main` still runs.
3. **Merge** the pull request once approved.
4. **Pull the merged `main`** locally before starting the next branch.

Suggested peer-review checklist for this module: inputs validated server-side,
duplicate email handled, membership codes unique, tests green, pages responsive.

### Merge conflict walkthrough

Conflicts are expected once two modules touch shared files such as
`app/__init__.py` (blueprint registration) or the navigation. Git marks the
overlapping lines with conflict markers:

```text
<<<<<<< HEAD
from .members.routes import bp as members_bp
=======
from .books.routes import bp as books_bp
>>>>>>> feature/book-management
```

Resolve by keeping **both** changes (the modules are independent), then:

```bash
# merge-style resolution
git add app/__init__.py
git commit

# ...or when rebasing onto main
git add app/__init__.py
git rebase --continue
```

Run the tests again after resolving, then push the branch so the pull request
updates. The commit history on this repository shows the same progression: scaffold
on `main`, then model, routes, UI and tests committed separately on
`feature/member-registration`.

## Notes and limitations

- No authentication or role management yet (course scope).
- Schema is created with `db.create_all()`; add Flask-Migrate if the schema starts
  evolving after the other modules land.
- The Book Management and Issue & Return modules can reference `Member` from
  `app.models` for loans and history once they are merged.
