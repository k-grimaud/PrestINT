# PrestINT

Outil web de gestion des prestations proposées par les clubs du BDA (TSP / IMT-BS), fondé sur une approche par **tickets**.

Cahier des charges complet : [`docs/cahier_des_charges.md`](docs/cahier_des_charges.md).

## Le projet

### Problème

Le BDA fédère de nombreux clubs qui proposent des prestations (animations, interventions, prêt de matériel…). Aujourd'hui, un client ne sait pas à qui s'adresser (BDA ? club ? les deux ?), personne n'a de vision de l'état d'avancement d'une demande, et chaque prestation est traitée comme un cas isolé sans réutiliser l'expérience des précédentes. Résultat : des allers-retours, des délais, et des demandes qui finissent oubliées.

### Objectif

Chaque demande devient un **ticket** avec un état, un historique et des interlocuteurs identifiés. Une **machine à états** encadre son cycle de vie (création, acceptation, refus, clôture…). Les prestations passées servent de base aux suivantes via des **templates** réutilisables.

### Fonctionnalités principales

**Côté client**

- Catalogue public (sans compte) : clubs → prestations d'un club → fiche détaillée
- Mise en favori et formulaire de demande de prestation
- Suivi des prestations en cours (statut, formulaire envoyé, chat dédié)
- Onglet notifications

**Côté club**

- Gestion des droits : président (admin général), responsable de prestation, collaborateurs
- Création / modification des prestations, de leur formulaire client et de leur template de gestion interne
- Une prestation en cours de modification n'est pas demandable par le client

**Planification et notifications**

- Diagrammes PERT / GANTT réutilisables, affectation de membres aux sous-tâches
- Synthèse de la prestation attribuée envoyée par chat et par mail ; rappels de jalons

**Contraintes** : Python, application web, limitation du nombre de demandes par utilisateur (anti-abus).

### Équipe et échéance

Erwan, Matteo, Krawlya — rendu le **9 décembre**.

## Stack technique

| Brique | Techno |
|---|---|
| Frontend | Vite + React + TypeScript |
| Backend | FastAPI (Python 3.13) |
| Base de données | PostgreSQL 17 |
| Orchestration | Docker Compose |

```
.
├── apps/
│   ├── caddy/      # Caddyfile (reverse proxy, https)
│   ├── frontend/   # Vite + React + TS, Dockerfile, .dockerignore
│   └── backend/    # FastAPI, requirements.txt, Dockerfile, .dockerignore
├── docker-compose.yml
└── docs/           # cahier des charges, cahiers de labo
```

## Lancer la stack

### Configuration .env

Un example de fichier .env est fournit dans .env.example

> Pour le moment, l'app ne fonctionne que pour les dev

### Lancer les conteneurs

Prérequis : Docker Desktop.

```sh
docker compose up --build -d   # première fois, ou après modification des dépendances
docker compose up -d        # ensuite
docker compose down         # arrêter
docker compose down -v      # arrêter ET réinitialiser la base
```

| Service | URL | Remarque |
|---|---|---|
| Application | https://prestint.localhost | via Caddy, seuls ports exposés publiquement : 443 (et 80, redirigé vers https) |
| Mails (Mailpit) | https://mail.prestint.localhost | via Caddy, capture tous les mails envoyés |
| API (Swagger) | http://localhost:8000/docs | accessible uniquement depuis la machine hôte |
| PostgreSQL | `127.0.0.1:5432` | identifiants dans `.env` — accessible uniquement depuis la machine hôte |

Vérification rapide que tout communique :

```sh
curl -k https://prestint.localhost/api/health   # → {"db":1}
```

> **Réseaux ignorés silencieusement.** Avec d'anciennes versions de Docker (constaté avec Engine 24 / Compose v2.19), un conteneur relié à plusieurs réseaux peut être créé sans l'un d'eux, sans aucune erreur (ex. `backend` sans `data` → `failed to resolve host 'db'`, `caddy` sans `mail_mock` → 502 sur Mailpit). Vérifier les réseaux d'un conteneur :
>
> ```sh
> docker inspect -f '{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}' prestint-backend-1
> ```
>
> Si un réseau manque : `docker network connect prestint_<réseau> prestint-<service>-1`. Mettre à jour Docker Desktop corrige le problème durablement.

## Schéma de la stack

```
Navigateur
   │  https://prestint.localhost          https://mail.prestint.localhost
   ▼                                                  │
┌──────────────┐                                      │
│    caddy     │ ◄────────────────────────────────────┘
│    :443      │ ──────────────────────────────────────────┐
└──────────────┘                                           ▼
       │                                           ┌──────────────┐
       ▼                                           │   mailpit    │
┌──────────────┐  /api/*  ┌──────────────┐  SMTP   │ :8025 / 1025 │
│   frontend   │ ───────► │   backend    │ ──────► └──────────────┘
│  Vite (dev)  │  proxy   │   FastAPI    │
│    :5173     │          │    :8000     │  DATABASE_URL  ┌──────────────┐
└──────────────┘          └──────────────┘ ─────────────► │      db      │
                                                          │ PostgreSQL 17│
                                                          │    :5432     │
                                                          └──────────────┘
   réseaux : edge (caddy, frontend, backend), data interne (backend, db),
             mail_mock interne (caddy, backend, mailpit)
```

- **Un seul point d'entrée.** Le navigateur ne parle qu'à Caddy (`:443`), qui relaie vers Vite (`frontend:5173`) ou Mailpit (`mailpit:8025`) selon le nom de domaine. Les certificats sont émis par l'autorité locale de Caddy : accepter l'avertissement du navigateur la première fois. Tout appel vers `/api/*` est relayé par le proxy de Vite (`server.proxy` dans `vite.config.ts`) vers `http://backend:8000`, cible fournie par la variable `VITE_PROXY_TARGET`. Même origine côté navigateur → pas de CORS à gérer.
- **Backend → base.** Le backend lit `DATABASE_URL=postgresql+psycopg://user:password@db:5432/prestint`. Le nom `db` est résolu par le DNS interne de Compose.
- **Ordre de démarrage.** `db` a un `healthcheck` (`pg_isready`) ; `backend` déclare `depends_on: db: condition: service_healthy` et ne démarre donc qu'une fois Postgres prêt.
- **Ports.** Seuls `443` et `80` (Caddy) sont publiés sur toutes les interfaces ; `8000` et `5432` ne sont liés qu'à `127.0.0.1` (confort de dev depuis la machine hôte, invisibles depuis l'extérieur).
- **Hot-reload.** Les dossiers `apps/backend` et `apps/frontend` sont montés dans les conteneurs : uvicorn tourne avec `--reload`, Vite fait du HMR. Un volume anonyme `/app/node_modules` conserve les modules Linux installés dans l'image plutôt que ceux de la machine hôte.
- **Persistance.** Les données Postgres vivent dans le volume nommé `postgres_data` (supprimé par `down -v`).
- **Images propres.** Les `.dockerignore` excluent `node_modules`, `dist`, `__pycache__`, `.venv`, `.env` du contexte de build.

## Développement

- Les routes backend doivent être préfixées par `/api` pour passer par le proxy. `apps/backend/main.py` contient pour l'instant un stub `GET /api/health` qui exécute `SELECT 1` sur la base.
- Les identifiants Postgres viennent de `.env` : changer les valeurs de `.env.example` avant tout déploiement.
