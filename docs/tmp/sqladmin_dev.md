# Dev-only DB viewer with sqladmin

> A guide, not a solution. You write the code; this tells you what goes where and why.

**Goal:** in dev, open <http://localhost:8000/admin> and browse every table in the PrestINT database. In prod, `/admin` doesn't exist.

**Effort:** one dependency and about 15 lines in `apps/backend/src/main.py`. No new container, compose service or Dockerfile change.

---

## 1. What sqladmin is

[sqladmin](https://smithyhq.github.io/sqladmin/) is an admin panel for SQLAlchemy apps on FastAPI/Starlette, similar to Django's admin. It reads your **SQLAlchemy models** and builds web pages from them:

- ✅ it lists the rows of each model, with sorting, search and pagination,
- ✅ it shows a detail page per row,
- ✅ it can create, edit and delete rows (each can be switched off per model),
- ❌ it has **no raw SQL console**. For ad-hoc `SELECT`s, use `psql` or a desktop client (DBeaver, TablePlus…) on `127.0.0.1:5432`, which is already exposed by `docker-compose.yml`.
- ❌ it only shows tables you have a **model** for. Alembic's own `alembic_version` table won't appear, and that's fine.

It is mounted **inside your existing FastAPI app**, so it runs in the backend container you already have.

---

## 1b. Editing data, and sqladmin vs pgAdmin

**Editing costs nothing extra.** It's on by default. Once a model has its `ModelView`, the panel shows Create / Edit / Delete for that table. The only work is *restricting* it. Each view has three flags, `can_create`, `can_edit` and `can_delete`, all `True` by default. You need one line per flag you switch off.

Suggested split:

| Editable | Read-only |
|---|---|
| `users`, `permission`, `picture`, `list_service`, `ongoing_service` | `audit_events`, `sessions`, `rate_limits`, `otp_codes` |

Instead of repeating the 3 flags four times, write **one** read-only base class and make the 4 read-only views inherit from it.

### API: the `can_*` flags

| Flag | Default | What it switches |
|---|---|---|
| `can_create` | `True` | the "+ New" button and form |
| `can_edit` | `True` | the edit button and form |
| `can_delete` | `True` | the delete button |
| `can_view_details` | `True` | the detail page of one row |
| `can_export` | `True` | the CSV/JSON export button |
| `can_import` | `False` | CSV import |

They are **class attributes** on a view. Example with a generic `Book` model:

```python
from sqladmin import ModelView

# A base class: no `model=` here, so sqladmin doesn't register it as a table.
class ReadOnlyView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False

# A real view: inherits the 3 flags, and adds its model.
class BookLogAdmin(ReadOnlyView, model=BookLog):
    column_list = "__all__"
```

A view class without `model=` is legal. sqladmin simply treats it as a parent class, and that's what makes the base-class trick work.

Edits go through HTML forms built from your SQLAlchemy models, so the models' defaults and types apply.

⚠️ Postgres-specific types (`INET`, `JSONB` in `audit_events`) may have no form field, and their edit page could then fail to load. A read-only view avoids the problem. Open that table's pages once to check.

| | sqladmin | pgAdmin |
|---|---|---|
| Browse rows | ✅ | ✅ |
| Create / edit / delete rows | ✅ (per table) | ✅ (every table) |
| Raw SQL console | ❌ | ✅ |
| Schema changes (DDL) | ❌ | ✅, but in this repo **Alembic owns the schema**, so you shouldn't use it anyway |
| Setup | `uv add --dev` + ~15 lines | A separate install and a server connection to configure |
| Lives in the repo / shared with the team | ✅ | ❌ (each dev sets it up) |

**About pgAdmin's ["Server Deployment"](https://www.pgadmin.org/docs/pgadmin4/9.18/server_deployment.html) page:** it covers running pgAdmin as a *shared, multi-user web service* (behind a WSGI server or Apache, with server mode and logins). That's more than one developer on a laptop needs. If you ever want pgAdmin's SQL console, run it locally (the desktop app, or the `pgadmin4` PyPI package in desktop mode) and connect it to `127.0.0.1:5432`, which `docker-compose.yml` already exposes. Both tools can coexist.

---

## 2. Install it as a dev dependency

From `apps/backend`: `uv add --dev sqladmin`

Why the **dev group** is the right place (see the earlier `uv add --dev` lesson):

| Where | Does it get sqladmin? | Why |
|---|---|---|
| Prod image | ❌ No | The Dockerfile runs `uv sync --no-dev --locked`. |
| Dev container | ✅ Yes | `docker-compose.dev.yml` runs `uv run …` **without** `--no-sync`, so uv syncs the default groups (dev included) on startup. |
| Your laptop | ✅ Yes | A plain `uv sync` includes dev. |

So the package is physically absent from prod. This is a stronger guarantee than "it's installed but switched off".

Pulls in: starlette (already there through FastAPI), wtforms, jinja2 (already there), python-multipart. Commit both `pyproject.toml` **and** `uv.lock`. Otherwise `--locked` will fail, as you saw in the CI lesson.

---

## 3. Wire it into `main.py`

You already have the pattern you need, at `apps/backend/src/main.py:14`:
`openapi_url="/openapi.json" if os.getenv("DEV_DOCS") else None`.
That's a dev-only feature switched on by an env flag. Do the same thing.

### Steps

1. **After** `app = FastAPI(...)` is created, open an `if` block on the dev flag.
2. **Inside the block**, import `Admin` and `ModelView` from `sqladmin`.
   - ⚠️ The import must be *inside* the `if`. A top-of-file import would crash prod at startup, because the package isn't installed there.
3. Create the admin: `Admin(app, engine)`. `engine` already exists in `infra/database.py` and is already imported in `main.py`. sqladmin accepts a **sync** engine like yours.

   > **API:** `Admin(app, engine, base_url="/admin", title="Admin")`. The defaults are shown; you only need the first two arguments.
   >
   > ```python
   > admin = Admin(app, engine, title="Bookshop admin")
   > ```

4. For each model, declare a small class that inherits from `ModelView` and passes the model as a **class keyword argument** (`model=…`, written in the class header, not in the body). In the body, set `column_list`. The special value `"__all__"` shows every column, so you don't have to list them.

   > **API:** `class <Name>(ModelView, model=<Model>)`. Useful class attributes:
   >
   > | Attribute | Default | Example |
   > |---|---|---|
   > | `column_list` | only the primary key | `"__all__"` or `[Book.id, Book.title]` |
   > | `name` / `name_plural` | from the class name (`Book` / `Books`) | `name_plural = "Library"` |
   > | `icon` | none | `"fa-solid fa-book"` ([Font Awesome](https://fontawesome.com/search) class) |
   >
   > ```python
   > class BookAdmin(ModelView, model=Book):
   >     column_list = "__all__"
   >     icon = "fa-solid fa-book"
   > ```
   >
   > Without `column_list`, the list page shows **only the primary key**. That's why `"__all__"` matters here.

5. Register each class with `admin.add_view(...)`.

   > **API:** `admin.add_view(BookAdmin)`. Pass the **class**, not an instance (`BookAdmin`, not `BookAdmin()`).

### The models to register (9)

| File | Models |
|---|---|
| `infra/models/identity.py` | `Users` (already imported in `main.py`), `Permission`, `Picture`, `Ongoing_Service`, `List_Service` |
| `infra/models/audit.py` | `UserSession`, `AuditEvent`, `RateLimit`, `OtpCode` |

Nine near-identical classes are boring but obvious, and that's fine. If the repetition bothers you, you can build the classes in a loop over the models (look up the 3-argument form of `type()`). Be honest with yourself about whether that's clearer.

### Which flag?

- **Reuse `DEV_DOCS` (lazy option):** it's already `1` in `.env.example` and already passed in `docker-compose.dev.yml`. Nothing else to touch. The downside is that the name says "docs" while it now controls more than that.
- **Add a dedicated `DEV_ADMIN`:** clearer, but you must add it to `.env.example`, `.env` and the backend `environment:` in `docker-compose.dev.yml`. If you forget the compose part, the variable never reaches the container and `/admin` silently stays off.

Both are valid. Pick one and know why.

---

## 3b. Nice-to-have view options

None of these are needed to get started. Add them when a table gets annoying to browse.

| Attribute | Default | What it does |
|---|---|---|
| `column_searchable_list` | `[]` | Adds a search box that searches these columns. |
| `column_sortable_list` | `[]` | Makes these column headers clickable to sort. |
| `column_default_sort` | `[]` | The initial sort: `"col"`, `("col", True)` for descending, or a list of those tuples. |
| `column_labels` | `{}` | Renames column headers. |
| `page_size` | `10` | Rows per page. |
| `form_excluded_columns` | `[]` | Hides fields from the create/edit form (e.g. auto-generated ids, `created_at`). |

```python
class BookAdmin(ModelView, model=Book):
    column_list = "__all__"
    column_searchable_list = [Book.title]
    column_sortable_list = [Book.title, Book.published_at]
    column_default_sort = ("published_at", True)    # newest first
    column_labels = {Book.published_at: "Published"}
    page_size = 50
    form_excluded_columns = [Book.id, Book.created_at]
```

Columns can be given as model attributes (`Book.title`) or as strings (`"title"`). Prefer attributes where possible: a typo then fails immediately when the app starts (`AttributeError`), whereas a string typo only shows up when you open the page. The examples in sqladmin's docs use a string for `column_default_sort`, so do the same there.

---

## 4. Gotchas

- **Sensitive data is visible.** `sessions.id` is very likely the session identifier your auth cookie carries (check `authentification/session.py`), so anyone who sees it could reuse it. OTP codes are stored hashed (`code_hash`), which is less risky. In dev this is acceptable, and it's exactly why the panel must never reach prod. You can hide columns, but there are three traps:
  - `column_exclude_list` only hides a column on the **list** page. The **detail** page still shows it unless you also set `column_details_exclude_list`.
  - Setting `column_list` **and** `column_exclude_list` in the same class raises an error at startup.
  - If a **parent** class sets `column_list` (e.g. `"__all__"` in your `ReadOnlyView`), a child's `column_exclude_list` is **silently ignored**, because the include list wins. Keep `column_list` out of shared base classes if you plan to exclude columns.

  ```python
  class SessionAdmin(ReadOnlyView, model=Session):
      column_exclude_list = [Session.token]          # hidden from the list page
      column_details_exclude_list = [Session.token]  # hidden from the detail page
  ```
- **Edits are real.** Create/edit/delete write to your dev database. Use `can_create`, `can_edit` and `can_delete` (all `True` by default) on a view to make it read-only, for example for `audit_events`.
- **No login screen by default.** The panel only exists in dev and the backend port is bound to `127.0.0.1`, so only your machine can reach it. If you still want a login, see §6.
- **Flag set in prod by mistake?** The import inside the `if` raises `ModuleNotFoundError` and the app refuses to start. That's loud and safe, which is the behaviour you want.
- **URL:** the panel is served by the **backend** (`:8000/admin`), not through the Vite proxy (`:5173/api`).

---

## 5. Verify

1. `docker compose up --build`, then watch the backend logs. On startup uv should install sqladmin into the dev venv.
2. Open <http://localhost:8000/admin>. You should see 9 entries in the sidebar. Click `Users` and you should see your rows.
3. Turn the flag off (remove it from `.env`), then restart the backend. `/admin` should now return **404**.
4. Prove prod is clean: build the image on its own with `docker build apps/backend`, then run `uv pip list` inside it. sqladmin must **not** be listed.

## 6. Adding a login

sqladmin has a built-in login page. You only supply the logic that decides "is this person allowed?", by subclassing `AuthenticationBackend`.

### How it works

```
browser → /admin/...  →  authenticate(request)  →  True:  page shown
                                              →  False: redirect to /admin/login
/admin/login (form)  →  login(request)        →  True:  remember them in a signed cookie
/admin/logout        →  logout(request)       →  forget them
```

"Remember them" uses Starlette's `SessionMiddleware`: `request.session` is a dict that is stored in a **signed** cookie. The browser can read it but can't forge it without your `secret_key`.

### Step 1: install the extra

The signed cookie needs `itsdangerous`, which isn't in your lockfile yet. Install sqladmin with its `auth` extra:
`uv add --dev "sqladmin[auth]"`

### Step 2: credentials and secret in `.env`

You need three new variables. Follow the `OTP_SECRET` pattern that's already there:
- in `.env.example`, as placeholders,
- in `.env`, with real values,
- in the backend `environment:` of `docker-compose.dev.yml`. If you forget this one, the container never sees the variables.

| Variable | Purpose |
|---|---|
| `ADMIN_USER` | the login name |
| `ADMIN_PASSWORD` | the password |
| `ADMIN_SECRET_KEY` | signs the session cookie. Generate it like `OTP_SECRET`. |

### Step 3: the backend class

You write three `async` methods. Here is the API, with a generic example:

| Method | Called when | Return |
|---|---|---|
| `login(self, request)` | the login form is submitted | `True` = success (you set something in `request.session`), `False` = "invalid credentials" |
| `logout(self, request)` | the logout button is clicked | `True` (after `request.session.clear()`) |
| `authenticate(self, request)` | **every** admin page | `True` = let them in, `False` = redirect to the login page |

```python
from sqladmin.authentication import AuthenticationBackend

class MyAuth(AuthenticationBackend):
    async def login(self, request):
        form = await request.form()   # fields are named "username" and "password"
        ok = secrets.compare_digest(form["username"], EXPECTED_USER) and \
             secrets.compare_digest(form["password"], EXPECTED_PASSWORD)
        if ok:
            request.session["admin"] = True
        return ok

    async def logout(self, request):
        request.session.clear()
        return True

    async def authenticate(self, request):
        return request.session.get("admin", False)
```

- `secrets.compare_digest` (from the standard library) instead of `==`: it takes the same time whether the first or the last character is wrong, so an attacker can't guess the password letter by letter from response times.
- Read the env variables with `os.environ["ADMIN_USER"]`, not `os.getenv`. If one is missing, the app should fail loudly at startup. With `getenv` you'd get `None`, and the comparison would raise `TypeError` at the first login attempt instead.
- Put the class **inside** your `if os.getenv("DEV_DOCS"):` block, like the views. That way prod never imports sqladmin.

### Step 4: plug it into `Admin`

> **API:** `Admin(app, engine, ..., authentication_backend=MyAuth(secret_key=..., session_cookie="admin_session"))`

⚠️ **Don't skip `session_cookie="admin_session"`.** By default the signed cookie is named **`session`**, which is exactly the name of your app's login cookie (`SESSION_COOKIE = "session"` in `authentification/session.py`). Cookies are shared across ports on `localhost`, so `:5173` (the frontend) and `:8000` (the admin) see the same cookie jar. Without a distinct name, logging into the admin would log you out of the app, and the reverse. (Verified: without the kwarg, the response sets `session=…`. With it, it sets `admin_session=…`.)

### Verify

1. Open `/admin`. You should be redirected to `/admin/login`.
2. Log in with the wrong password. You should get an error message and stay on the login page.
3. Log in with the right password. The tables should show.
4. Log into the **app** (OTP) in the same browser, then reload `/admin`. You should still be logged in to both, which proves the cookie names don't collide.
5. Click logout. You should be back on the login page.

### Going further (not needed now)

Your users already log in through OTP. Instead of a separate password, `authenticate` could read the app's `session` cookie (`request.cookies`), run the same query as `get_current_user`, and check the `permission` table for an admin role. That's what you'd want if the panel ever runs outside dev. Then `login` would just redirect to the frontend login page.

---

## References

- sqladmin docs: <https://smithyhq.github.io/sqladmin/>
- Configuration (`column_list`, `column_exclude_list`, `can_*`): <https://smithyhq.github.io/sqladmin/configurations/>
- Authentication: <https://smithyhq.github.io/sqladmin/authentication/>
