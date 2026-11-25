# UML — modèles SQLAlchemy

Source : `apps/backend/src/infra/models/` (identity.py, audit.py). Toutes les classes héritent de `Base(DeclarativeBase)`.

```mermaid
classDiagram
    direction LR

    class Association {
        <<association>>
        +varchar50 asso_id PK
        +varchar50 name
        +varchar15 status
    }
    class Users {
        <<users>>
        +UUID user_id PK
        +varchar255 email UNIQUE sur lower(email)
        +varchar500 password_hashed
        +varchar50 first_name
        +varchar50 last_name
    }
    class Permission {
        <<permission>>
        +varchar50 asso_id PK FK
        +UUID user_id PK FK
        +varchar15 permission
    }
    class Picture {
        <<picture>>
        +UUID picture_id PK
        +varchar50 asso_id FK
        +varchar512 path
    }
    class List_Service {
        <<list_service>>
        +UUID list_service_id PK
        +varchar50 asso_id FK
        +varchar255 name
        +int approximative_cost
        +varchar50 approximative_time
        +varchar255 description
        +varchar512 path
    }
    class Ongoing_Service {
        <<ongoing_service>>
        +UUID service_id PK
        +varchar50 asso_id FK
        +UUID client_id FK
        +UUID type_service_id FK
        +timestamptz created_at défaut now()
        +timestamptz? end_at
        +varchar25 status
        +varchar255 context
    }
    class UserSession {
        <<sessions>>
        +UUID id PK
        +UUID user_id FK
        +timestamptz created_at défaut now()
        +timestamptz expires_at
        +timestamptz? revoked_at
    }
    class AuditEvent {
        <<audit_events>>
        +int id PK
        +timestamptz occurred_at défaut now()
        +UUID? user_id FK
        +INET ip
        +str event_type
        +JSONB? detail
    }
    class RateLimit {
        <<rate_limits>>
        +str bucket PK
        +int count défaut 0
        +timestamptz expires_at
    }
    class OtpCode {
        <<otp_codes>>
        +UUID id PK
        +varchar255 email INDEX
        +varchar64 code_hash
        +timestamptz created_at défaut now()
        +timestamptz expires_at
        +int attempts défaut 0
        +timestamptz? consumed_at
    }

    Association "1" -- "0..*" Permission
    Users "1" -- "0..*" Permission
    Association "1" -- "0..*" Picture
    Association "1" -- "0..*" List_Service
    Association "1" -- "0..*" Ongoing_Service
    Users "1" -- "0..*" Ongoing_Service : client_id
    List_Service "1" -- "0..*" Ongoing_Service : type_service_id
    Users "1" -- "0..*" UserSession
    Users "0..1" -- "0..*" AuditEvent
```

**Légende — fichier source** (`apps/backend/src/infra/models/`)

| Fichier | Classes |
|---|---|
| `identity.py` | Association, Users, Permission, Picture, List_Service, Ongoing_Service |
| `audit.py` | UserSession, AuditEvent, RateLimit, OtpCode |

Remarques :
- `?` = colonne nullable. Stéréotype = nom de la table.
- `RateLimit` et `OtpCode` sont isolées (aucune clé étrangère).
