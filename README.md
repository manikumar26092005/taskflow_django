# TaskFlow — Django To-Do App

A re-styled version of the TaskFlow app: same features (register/login, dashboard
stats, add/edit/delete/complete tasks, search & filter, categories), new look —
a warm "paper & ink" theme (deep forest green + sage, Fraunces/Inter type)
instead of the original purple gradient.

## Setup

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install Django
pip install django

# 3. Apply migrations
python manage.py migrate

# 4. (Optional) create an admin user
python manage.py createsuperuser

# 5. Run the dev server
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** — you'll land on the login page. Click
"Register here" to create an account, then you're in.

## What's inside

- `tasks/` — the Django app: models (`Task`, `Category`), views, forms, urls
- `templates/` — all HTML (base layout, auth pages, task list/form, categories)
- `static/css/style.css` — the whole visual identity in one file
- `taskflow_project/` — project settings/urls/wsgi

## Notes

- `SECRET_KEY` in `settings.py` is a placeholder — replace it before deploying
  anywhere public.
- SQLite is used by default (`db.sqlite3`, created on first `migrate`).
- Tasks are scoped per logged-in user; categories are too.
- The "Filter" bar supports search by title, status (pending/completed),
  priority, and category — all via GET params, so filtered views are
  shareable/bookmarkable links.
