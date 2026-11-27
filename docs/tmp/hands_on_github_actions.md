# Hands-on: GitHub Actions from scratch

> A lesson, not a solution. You write every line of YAML yourself.
> When you get stuck, the hints point you to the right doc page. They won't hand you the answer.

**Goal by the end:** every `git push` to GitHub runs black, ruff, oxlint and a TypeScript type check on PrestINT. If anything is badly formatted or broken, you get a red ❌.

---

## 1. What CI/CD actually is

**CI (Continuous Integration):** every time code reaches the shared repo, a machine you don't own checks it automatically. It installs deps, then runs the formatters, linters and tests. The point is to catch problems *before* they pile up, and to make sure the check never depends on "it works on my laptop".

**CD (Continuous Delivery/Deployment):** once CI is green, the same machinery *ships* the code. It builds Docker images, pushes them to a registry and deploys to a server. CD is out of scope here (see §10).

A key mindset: **CI checks, it doesn't fix.** A formatter in CI runs in *check mode*. It says "this file isn't formatted" and fails. You fix it locally and push again. A bot that rewrites your code on the server and commits it is possible, but it's a separate, more advanced pattern. Avoid it for now.

---

## 2. Vocabulary and the mental model

```text
  you: git push
        │
        ▼
  ┌──────────── EVENT (push, pull_request, ...) ────────────┐
  │                                                         │
  │  WORKFLOW  = one YAML file in .github/workflows/        │
  │   │                                                     │
  │   ├── JOB "backend"   ──► runs on its own fresh VM      │
  │   │     step 1  (uses: an action)                       │
  │   │     step 2  (run: a shell command)                  │
  │   │     step 3  ...        steps = sequential           │
  │   │                                                     │
  │   └── JOB "frontend"  ──► another fresh VM              │
  │         step 1 ...         jobs = parallel by default   │
  └─────────────────────────────────────────────────────────┘
```

| Term | Meaning |
|---|---|
| **Event** | What triggers the workflow: a push, a PR, a cron schedule, a manual button. |
| **Workflow** | One `.yml` file under `.github/workflows/`. A repo can have many. |
| **Job** | A group of steps that runs on **one runner**. Jobs run **in parallel** unless you chain them. |
| **Runner** | The VM that executes a job. `ubuntu-latest` is a GitHub-hosted Linux VM. It is **brand new and empty** every time. |
| **Step** | One unit of work inside a job. Steps run **in order**, and they share the same filesystem. |
| `run:` | A step that runs a shell command (bash on Ubuntu). |
| `uses:` | A step that calls an **action**, a reusable packaged step written by someone else (or you). |
| **Action** | Like a function from a library. It is versioned, takes inputs through `with:`, and lives in a GitHub repo. |

**The most important consequence:** the runner starts empty. Your code isn't there, and neither is Python, uv or your `node_modules`. Every job must:

1. Fetch the code.
2. Install the tools it needs.
3. Install the project's deps.
4. Run the checks.

Nearly every CI job in the world follows this four-beat rhythm. Memorise it.

---

## 3. Anatomy of a workflow file

Files live at `.github/workflows/<anything>.yml`. GitHub picks up every file in that folder.

Top-level keys you'll meet, from outside to inside:

- **`name`**: label shown in the Actions tab. Optional.
- **`on`**: the trigger(s). See §4.
- **`env`**: environment variables for the whole workflow (they can also be set per job or per step).
- **`jobs`**: a map. Each key is a job id that *you* choose (e.g. `backend`, `frontend`).
  - **`runs-on`**: which runner (`ubuntu-latest` almost always).
  - **`needs`**: makes this job wait for another job. That's how you chain jobs (e.g. "deploy needs tests").
  - **`if`**: a condition for running the job or step (e.g. only on `main`).
  - **`strategy.matrix`**: runs the same job several times with different values (e.g. Python 3.12 *and* 3.13). Not needed here, but good to know it exists.
  - **`defaults.run.working-directory`**: the folder that every `run:` step in this job executes in. **Very useful in a monorepo like ours.**
  - **`steps`**: a **list** (each item starts with `-`). Each step has either `uses:` or `run:`, plus optionally:
    - `name:` (label in the logs)
    - `with:` (inputs for an action)
    - `working-directory:` (per-step folder)
    - `env:`

### YAML gotchas (where beginners lose an hour)

- **Indentation is syntax.** Use spaces only, never tabs. A step indented one space off becomes something else entirely.
- **`-` means "list item", `key:` means "map entry".** `steps` is a list of maps. `jobs` is a map of maps.
- `on: [push, pull_request]` and the multi-line form, with `on:` followed by indented `push:`, mean the same thing. You need the multi-line form as soon as you want to add filters.
- Multi-line shell commands use `run: |` followed by indented lines.
- When a workflow file is invalid, GitHub shows the error in the Actions tab instead of running it. Read that message. It usually gives the line number.

---

## 4. Triggers (`on:`) in depth

- **`push`**: fires on every push to any branch, unless you filter it.
- **`pull_request`**: fires when a PR is opened or updated. It runs against the *merge result* of your branch with the target branch.
- Having **both** means a push to a branch that has an open PR runs the workflow twice. That's common and acceptable. Some people restrict `push` to `main` to avoid it.
- **Branch filters**: `branches:` under `push`/`pull_request` restricts which branches trigger the workflow.
- **Path filters**: `paths:` restricts triggering to changes in certain files. **This matters for a monorepo:** why run the frontend linter when you only touched `apps/backend/`?
  - Gotcha: `paths` applies to the **whole workflow**, not to a single job. If you want backend and frontend filtered independently, the simplest route is **two workflow files**.
- **`workflow_dispatch`**: adds a "Run workflow" button in the Actions tab. It's handy while you learn.

📖 Doc to read: *"Events that trigger workflows"* and *"Workflow syntax → on.push.paths"*.

---

## 5. Actions: the reusable bricks

You won't reinvent setup steps. These five will cover 90% of your needs:

| Action | What it does | Latest major (Oct 2026) |
|---|---|---|
| `actions/checkout` | Clones your repo into the runner. **Without it, the runner has no code.** | v7 |
| `actions/setup-python` | Installs a given Python version. | v7 |
| `astral-sh/setup-uv` | Installs **uv** and can cache its downloads. (It can also provide Python.) | `v10.3.0`. ⚠️ No `@v10` major tag exists, so you must use the full version. |
| `actions/setup-node` | Installs Node, and can cache npm downloads (`cache: npm`). | v7 |
| `psf/black` | Runs black directly, with no Python setup required. | `@stable` |

### Versions after the `@`

- `@v7` is a **major tag**. You get bug fixes automatically, with no breaking changes. This is the normal choice.
- `@stable` / `@main` is a **moving branch**, so it can change under you at any time. It's convenient but less reproducible.
- `@<40-char commit SHA>` is **fully pinned**. It's the most secure option and is what security-conscious orgs use. Don't bother with it yet.

### How to know which inputs (`with:`) an action accepts

Open the action's GitHub repo and read its **README** or its **`action.yml`**. The `inputs:` section lists every option and its default. **Build this habit.** It answers most "how do I…" questions.

---

## 6. Dissecting your current `black.yml`

You already have this (staged in git):

```yaml
name: Lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: psf/black@stable
```

Line by line:

1. `name: Lint` is the label in the Actions tab.
2. `on: [push, pull_request]` runs on every push to every branch, and on every PR.
3. `jobs:` → `lint:` defines one job, with id `lint`.
4. `runs-on: ubuntu-latest` runs it on a fresh Ubuntu VM.
5. `actions/checkout@v6` brings your code in. (v7 exists now. Bump it.)
6. `psf/black@stable` runs black. Its `action.yml` shows these defaults:
   - `options: "--check --diff"` → **check mode**. It fails if a file would change, and it prints the diff. It never rewrites anything. ✅ That's what you want.
   - `src: "."` → it scans **the whole repo**. ⚠️ That's not ideal here.
   - `version: ""` → it uses whatever black version matches the action ref. ⚠️ That version may differ from the one you run locally, so CI and your laptop can disagree.
   - `use_pyproject: "false"` → if you turn it on, it reads the black version from `pyproject.toml` (`[tool.black] required-version`, or black listed in `[project]` deps or `[dependency-groups]`). ⚠️ **But it only looks at the repo root** (`./pyproject.toml`) and has no input to change that path. Here the file lives in `apps/backend/`, so it fails with `'with.use_pyproject' input requires a pyproject.toml file.` It works for single-project repos, but not for this monorepo.

**Questions for you to answer (look at the inputs above):**

- How do you tell it to scan only `apps/backend`?
- `use_pyproject` is out (see above). So how do you make CI use *exactly* the same black version as your laptop? (Two answers: pin it by hand with `version:`, which you then have to keep in sync, or drop the action and run `uv run black` from the lockfile, as in Ex 3.)

---

## 7. The tools and why

### Backend (Python, `apps/backend/`, managed by **uv**)

| Tool | Role | Check-mode flag to look up |
|---|---|---|
| **black** | Formatter. It decides how code *looks*, with no debates. | `--check` (+ `--diff`) |
| **ruff** | Very fast linter: unused imports, undefined names, import order (with the `I` rules), and more. It can *also* format, but you're using black for that. | `ruff check` (lint). Look up how to enable the `I` rule set in `pyproject.toml`. |

**Good practice:** add both as **dev dependencies** with uv (look up `uv add --dev`). Then:

- The versions are pinned in `uv.lock`.
- You run `uv run black …` / `uv run ruff …` locally.
- CI runs **the exact same commands**, so there are no surprises.

Once you do this, you don't strictly need the `psf/black` action anymore: CI can just call `uv run black --check …`. Decide which approach you prefer, and know why.

Configuration lives in `apps/backend/pyproject.toml` under `[tool.black]` and `[tool.ruff]`. Look up `line-length` and `target-version` and set them consistently for both tools.

### Frontend (TS/React, `apps/frontend/`, managed by **npm**)

| Tool | Role | Already there? |
|---|---|---|
| **oxlint** | Linter (a fast eslint alternative). | ✅ `npm run lint` |
| **tsc** | Type checker. It catches type errors without building. | ✅ (`typescript` in devDependencies). Look up `tsc --noEmit` and the `-b` build mode used in your `build` script. |
| **prettier** | Formatter, the "black of JS". | ❌ Not installed. Your call whether you want it. If you do, its check flag is `--check`. |

**CI install tip:** in CI, use `npm ci`, not `npm install`. It installs *exactly* what `package-lock.json` says and fails if the lockfile is out of sync. That strictness is exactly what CI should do. The uv equivalent is `uv sync --locked` (look up `--locked` vs `--frozen`).

---

## 8. Hands-on exercises

Do them in order. Push after each one and watch the **Actions** tab on GitHub.

### Ex 1: Hello, runner
Create a throwaway workflow that triggers on push and on `workflow_dispatch`. It should have a single job with steps that:
- echo a message,
- print `pwd` and `ls -la` **before** checkout,
- check out the code,
- print `ls -la` again.

**Expected result:** the first `ls` is empty and the second shows your repo. Now you *understand* why checkout exists. Delete the file afterwards.

### Ex 2: Fix `black.yml`
- Bump checkout to the current major version.
- Make black scan only `apps/backend`.
- Push. Is it green? If not, run black locally, fix, and push again.
- **Then break it on purpose:** add ugly spacing to one backend file and push. Click into the failed run and find the diff in the logs. Revert.

**Expected result:** you've seen a ❌ and know how to read it.

### Ex 3: Backend job with uv + ruff
Replace (or extend) the black job with a "backend" job that follows the four beats from §2:
1. checkout
2. set up uv (hint: `astral-sh/setup-uv`). Caching is already on by default (`enable-cache: auto`), so you don't need to set it. Look at its `python-version` input (Python 3.13 must be available) and its `working-directory` input (where it looks for `pyproject.toml`).
3. install deps from the lockfile
4. run `black --check` and `ruff check` through `uv run`

**Hint:** `uv` needs to run *inside* `apps/backend` to find `pyproject.toml`. Two places to set that are a job-level `defaults` or a step-level `working-directory`.

**Expected result:** two separate check steps in the log, both green.

**Bonus question:** if black fails, does ruff still run? (Look up `if: always()` / `if: success() || failure()` and decide whether you want both reports every time.)

### Ex 4: Frontend job
Add a second job, `frontend`:
1. checkout
2. setup-node (pick a current LTS Node version, and find the input that caches npm, plus the one that tells it where the lockfile is in a subfolder)
3. `npm ci`
4. lint, then type check

**Expected result:** in the Actions UI, `backend` and `frontend` run **at the same time** (parallel jobs).

### Ex 5: Only run what changed
Using `paths` filters, make the backend checks run only when `apps/backend/**` (or the workflow file itself) changes, and likewise for the frontend.

**Hint:** reread the gotcha in §4. You'll probably end with two workflow files.

**Expected result:** a commit that only touches the frontend doesn't trigger the backend workflow.

### Ex 6 (bonus): Shift left
- **pre-commit hooks**: look up the `pre-commit` framework (or a plain `.git/hooks/pre-commit` script). It runs black/ruff *before* the commit is even created, so CI rarely fails.
- **Status badge**: each workflow has a badge URL (Actions tab → workflow → "…" → *Create status badge*). Put it in `README.md`.
- **Branch protection**: in repo Settings → Branches, require your checks to pass before merging into `main`. This is what makes CI *binding*.

---

## 9. When a run fails

1. **Actions tab** → click the run → click the red job → expand the red step. The real error is usually in the **last 10 lines**.
2. **Common causes:**
   - *"No such file or directory" / "pyproject.toml not found"*: wrong `working-directory`.
   - *Empty workspace*: you forgot `actions/checkout`.
   - *Lockfile out of sync*: you changed deps without committing `uv.lock` / `package-lock.json`.
   - *Passes locally, fails in CI*: the tool versions differ. Pin them (§7).
   - *Workflow doesn't appear at all*: invalid YAML, or the file isn't in `.github/workflows/`.
3. **Re-run**: the "Re-run jobs" button. "Re-run failed jobs" saves time.
4. **Debug logs**: set the repo secret `ACTIONS_STEP_DEBUG` to `true` for verbose output.
5. **Run locally**: the tool `act` simulates runners in Docker. It's nice to know about, but not required.

---

## 10. Where CD fits (later)

Once CI is solid, the next workflow typically:

- triggers only on push to `main` (or on a tag),
- uses `needs:` to wait for the CI jobs,
- builds your `apps/*/Dockerfile`s and pushes the images to a registry (GHCR is free with GitHub),
- deploys them (SSH to a server, a cloud service, …) using **secrets** (Settings → Secrets → `${{ secrets.NAME }}`), never hard-coded credentials.

Concepts to look up when you get there: *secrets*, *environments*, *permissions: (GITHUB_TOKEN)*, *docker/build-push-action*.

---

## 11. Going further: what else CI can check

Each item below says **what it catches**, **which tool** to use, **where** to put it, **what to set**, and **how you know it works**. There's no YAML: you write it, as for the exercises. Do the items in this order; each one builds on the previous.

Versions were checked in October 2026. ⚠️ Some actions have **no short major tag** (e.g. `@v3`), so `@v3` fails with "unable to find version". That's what happened with `setup-uv@v10`. When the table says "full tag", use the exact version.

| Action | Tag to use |
|---|---|
| `docker/setup-buildx-action` | `@v4` |
| `docker/build-push-action` | `@v7` |
| `hadolint/hadolint-action` | `@v3.5.0` (full tag) |
| `gitleaks/gitleaks-action` | `@v3` |
| `rhysd/actionlint` | not an action. Use its Docker image `rhysd/actionlint:1.7.12`. |

### 11.1 Check that the Docker images build ⭐

- **Catches:** a broken Dockerfile, a `COPY` of a file that doesn't exist, a lockfile out of sync (your backend Dockerfile runs `uv sync --locked`, so it fails exactly like CI should).
- **Tools:** `docker/setup-buildx-action`, then `docker/build-push-action`.
- **Where:** a **new job** (e.g. `backend-image`) in `backend.yml`, and the same in `frontend.yml`. It's a separate job, so it runs in parallel with lint, and the path filters already apply.
- **What to set:**
  - Steps: checkout, setup-buildx (no inputs), build-push.
  - build-push inputs: `context` = the app folder (`apps/backend` or `apps/frontend`), `push` = false (build only, publish nothing).
  - Caching, so builds don't start from zero every time: `cache-from` = the GitHub Actions cache type (`type=gha`), and `cache-to` = the same type with `mode=max`, so every layer is cached.
- **Done when:** the job is green. Break it on purpose (add a typo to a `COPY` line) and it should turn red.

### 11.2 Frontend production build

- **Catches:** errors that only appear when Vite bundles the app, such as a wrong import path, a missing asset or a broken `vite.config.ts`. `tsc -b` doesn't see these.
- **Tool:** your existing `build` script (`npm run build` = `tsc -b && vite build`).
- **Where:** `frontend.yml`, in the lint job, after `npm ci`.
- **What to change:** since `build` already runs `tsc -b`, **replace** the `npx tsc -b` step with `npm run build` instead of running the type check twice.
- **Done when:** the log shows Vite's "built in …" line.

### 11.3 Check the database migrations ⭐

- **Catches:** a migration that fails on an empty database, and a **model changed without a migration**.
- **Tools:**
  - GitHub **service containers**, which start a Postgres next to the job;
  - `alembic upgrade head`;
  - `alembic check`, which fails if your models and your migrations disagree.
- **Where:** a new job (e.g. `migrations`) in `backend.yml`.
- **What to set:**
  - `services:` with one entry, `postgres`:
    - `image` = `postgres:17` (same as compose);
    - `env` = the three `POSTGRES_*` variables with throwaway values;
    - `ports` = map 5432 to 5432;
    - `options` = a health check using `pg_isready`, the same idea as the healthcheck in `docker-compose.yml`. Without it, the job starts before Postgres is ready.
  - At job level, `env`: `DATABASE_URL` pointing at `localhost:5432` with those throwaway credentials and the `postgresql+psycopg://` prefix your app uses. `alembic/env.py` reads it with `os.environ`, so it's required.
  - `defaults.run.working-directory` = `apps/backend`. `alembic.ini` is there, and it already adds `src` to the import path.
  - Steps: checkout, setup-uv, `uv sync --locked`, then `uv run alembic upgrade head`, then `uv run alembic check`.
- ⚠️ **Fix this first:** `alembic check` compares the DB with `Base.metadata`. Your `alembic/env.py` imports `Base` from `infra.database` but **never imports the models** (`infra.models`), so the metadata is empty. `alembic check` would then think every table should be dropped and fail. Add an import of `infra.models` in `env.py`; that package's `__init__.py` already imports `audit` and `identity`. Check locally first, against your compose DB, with `uv run alembic check`.
- **Done when:** both steps are green. Add a column to a model without generating a migration, and `alembic check` should turn red.

### 11.4 Dependabot: keep dependencies up to date

- **Catches:** outdated actions (like the `@v10` tag problem), npm packages and Python packages, including ones with known security holes.
- **Tool:** Dependabot, built into GitHub. It's a config file, not a workflow.
- **Where:** a new file, `.github/dependabot.yml`.
- **What to set:**
  - `version` = 2.
  - `updates` = a list of three entries, each with `package-ecosystem`, `directory` and `schedule.interval` (`weekly` is a calm default):

    | `package-ecosystem` | `directory` |
    |---|---|
    | `github-actions` | `/` |
    | `npm` | `/apps/frontend` |
    | `uv` | `/apps/backend` |

  - Optional: `groups`, to bundle minor updates into one PR instead of one PR per package.
- **Done when:** Dependabot PRs appear under **Pull requests**, and your path-filtered workflows run on them automatically.

### 11.5 Lint the CI files and the Dockerfiles themselves

- **Catches:**
  - **actionlint:** mistakes in workflow files before they run, e.g. `with:` on a `run:` step, an unknown key like `src:` on a job, or a typo in an expression;
  - **hadolint:** Dockerfile bad practices, e.g. unpinned versions, `apt-get` without cleanup, or needless layers.
- **Tools:** the `rhysd/actionlint:1.7.12` Docker image, run with `docker run` in a `run:` step (mount the repo, set the workdir to it, pass `-color`); `hadolint/hadolint-action@v3.5.0`, input `dockerfile` = the path to each Dockerfile.
- **Where:** a new workflow, e.g. `meta.yml`, path-filtered on `.github/workflows/**` and `apps/*/Dockerfile`. Or put hadolint in each app's workflow with its own Dockerfile.
- **What to set:** for hadolint, optionally `failure-threshold` (e.g. `warning`), so style-only notes don't fail the build.
- **Done when:** break a workflow on purpose (put `with:` under a `run:` step) and actionlint points at the exact line.

### 11.6 Workflow hygiene

- **Catches:** wasted runner minutes and stuck jobs.
- **What to set:**
  - `concurrency`, at workflow level:
    - `group` = an expression combining the workflow name (`github.workflow`) and the branch/ref (`github.ref`);
    - `cancel-in-progress` = true.

    If you push twice quickly, the run for the older commit is cancelled.
  - `timeout-minutes` on each job, e.g. 10. A stuck job then stops after 10 minutes instead of the default 6 hours.
- **Where:** every workflow file.

### 11.7 Smoke test the whole stack

- **Catches:** "each part builds, but they don't work together", e.g. the backend can't reach the DB, a wrong env variable, or a migration that crashes on startup.
- **Tools:** Docker Compose (preinstalled on the runner) and `curl`.
- **Where:** a new workflow, e.g. `stack.yml`, with no path filter (or filtered on `apps/**` plus the compose files), because it tests everything together.
- **What to change:**
  - Compose needs a `.env`, which isn't in the repo (good). Add a step that **copies `.env.example` to `.env`**, then fills in any secret it needs with a throwaway value (`OTP_SECRET`, …).
  - Steps:
    1. checkout and the `.env` step;
    2. `docker compose up -d --wait`, where `--wait` blocks until the healthchecks pass;
    3. `curl --fail` on `http://localhost:8000/api/health`, which runs `SELECT 1`, so it proves backend → Postgres;
    4. `docker compose down -v`, with `if: always()` so it runs even after a failure.
- **Done when:** the curl step prints `{"db":1}`.

### 11.8 Real tests (once you write some)

You have none yet. When you do:

- **Backend:** `pytest` as a dev dependency (`uv add --dev pytest`), and a `uv run pytest` step. If tests need a DB, reuse the Postgres service and `DATABASE_URL` from 11.3.
- **Frontend:** **Vitest** (it fits with Vite) as a dev dependency, a `"test"` script in `package.json` (Vitest's run-once mode, not watch mode), and an `npm test` step.

### 11.9 Security scans

- **`npm audit`:** a `run:` step in `frontend.yml` after `npm ci`, with `--audit-level=high`, so only serious issues fail the build.
- **gitleaks:** `gitleaks/gitleaks-action@v3` scans commits for leaked secrets, such as a `.env` value or a token pasted into code.
  - The checkout step needs `fetch-depth` = 0, so the full history is available to scan.
  - Pass `GITHUB_TOKEN` (from `secrets`) as an `env` variable.
  - No license key is needed, because this repo belongs to a personal account, not an organization.

---

## 12. Checklist

- [ ] I can explain event → workflow → job → step, and the difference between `uses` and `run`.
- [ ] I know why every job starts with checkout.
- [ ] I can find an action's inputs by reading its `action.yml`.
- [ ] black and ruff run in check mode on `apps/backend`, with versions pinned through uv.
- [ ] oxlint and the type check run on `apps/frontend` after `npm ci`.
- [ ] Each part only runs when its folder changes.
- [ ] I've seen a red run, read its logs, and fixed it.
- [ ] (Bonus) pre-commit hooks, a badge, branch protection.
- [ ] (§11) Docker images build in CI, with layer caching.
- [ ] (§11) The frontend production build runs in CI.
- [ ] (§11) Migrations apply to an empty Postgres, and `alembic check` is green.
- [ ] (§11) Dependabot is configured for actions, npm and uv.
- [ ] (§11) actionlint and hadolint run, plus `concurrency` and `timeout-minutes` everywhere.

## References

- Workflow syntax: <https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions>
- Events: <https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows>
- psf/black action: <https://black.readthedocs.io/en/stable/integrations/github_actions.html>
- uv in GitHub Actions: <https://docs.astral.sh/uv/guides/integration/github/>
- ruff configuration: <https://docs.astral.sh/ruff/configuration/>
- setup-node: <https://github.com/actions/setup-node>
- build-push-action (and its cache docs): <https://github.com/docker/build-push-action>
- Service containers (Postgres): <https://docs.github.com/en/actions/use-cases-and-examples/using-containerized-services/creating-postgresql-service-containers>
- Dependabot options: <https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference>
- actionlint: <https://github.com/rhysd/actionlint/blob/main/docs/usage.md>
- hadolint-action: <https://github.com/hadolint/hadolint-action>
- gitleaks-action: <https://github.com/gitleaks/gitleaks-action>
