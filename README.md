# Task Tracker

A full-stack task management application built with FastAPI, Vue 3, and PostgreSQL. Allows users to create, update, and delete tasks with real-time UI updates.

This project was built as part of an IT Developer Intern technical assessment at PT Global Loyalty Indonesia (Alfagift).

## Features

- **Create, read, update, delete tasks** via REST API
- **Three status workflow:** Todo → In Progress → Done
- **Real-time UI updates** without page reload
- **Client and server-side validation** with informative error messages
- **Responsive design** that works on mobile and desktop
- **Auto-generated API documentation** via Swagger UI
- **Production-ready architecture:** layered backend, service layer frontend
- **Auto-database initialization** on first run

## Tech Stack

### Backend
- **Python 3.12** with **FastAPI 0.138** — modern async web framework
- **SQLAlchemy 2.0** — ORM with declarative models
- **PostgreSQL 18** — relational database
- **Pydantic v2** — data validation and serialization
- **Uvicorn** — ASGI server
- **python-dotenv** — environment variable management

### Frontend
- **Vue 3** with **Composition API** — reactive UI framework
- **Vite** — build tool and dev server
- **Axios** — HTTP client
- **Tailwind CSS v4** — utility-first CSS framework

## Architecture

The application follows a 3-tier architecture with clear separation of concerns:

```
Frontend (Vue 3)  ──HTTP/JSON──►  Backend (FastAPI)  ──SQL──►  Database (PostgreSQL)
   Port 5173                         Port 8000                     Port 5432
```

### Backend (Layered Architecture)

Each layer has a single responsibility and depends only on the layer below it:

- **Routers** (`app/routers/`) — HTTP endpoint handlers
- **Schemas** (`app/schemas/`) — Pydantic models for request/response validation
- **CRUD** (`app/crud/`) — Business logic and database operations
- **Models** (`app/models/`) — SQLAlchemy ORM models (table definitions)
- **Database** (`app/database.py`) — Connection, session management, dependency injection

Request flow: `Router → Schema (validation) → CRUD → Model → Database`

### Frontend (Component + Service Layer)

- **Components** (`src/components/`) — Vue Single File Components for UI
- **Services** (`src/services/`) — API client abstraction (Axios calls centralized)

Request flow: `Component → Service → Axios → Backend`

## Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.10 or higher** (developed with 3.12)
- **Node.js 18 or higher** (developed with 22 LTS)
- **PostgreSQL 14 or higher** (developed with 18)
- **Git**

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd task-tracker
```

### 2. Database Setup

Create a PostgreSQL database for the application:

```bash
psql -U postgres
```

In the PostgreSQL shell:

```sql
CREATE DATABASE task_tracker;
\q
```

### 3. Backend Setup

Navigate to the backend directory and create a virtual environment:

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file from the template:

**Windows:**
```bash
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

Edit `.env` and fill in your PostgreSQL credentials:

```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_NAME=task_tracker
```

Run the backend server:

```bash
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`.
Swagger UI documentation: `http://localhost:8000/docs`

The database table will be created automatically on first run.

### 4. Frontend Setup

Open a **new terminal** (keep the backend running). Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create the environment file from the template:

**Windows:**
```bash
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

The default `.env` points to the local backend:

```
VITE_API_URL=http://127.0.0.1:8000
```

Run the frontend dev server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

### Quick Verification

After both servers are running:

1. Open `http://localhost:5173` in your browser — you should see the Task Tracker UI
2. Open `http://localhost:8000/docs` — you should see the Swagger API documentation
3. Try creating a task via the UI — it should appear in the list immediately

## API Documentation

The API follows REST conventions. All endpoints return JSON.

Base URL: `http://localhost:8000`

Interactive documentation available at `http://localhost:8000/docs` (Swagger UI).

### Endpoints

| Method | Endpoint | Description | Success Status |
|--------|----------|-------------|----------------|
| GET | `/tasks` | Retrieve all tasks | 200 OK |
| POST | `/tasks` | Create a new task | 201 Created |
| PUT | `/tasks/{id}` | Update an existing task | 200 OK |
| DELETE | `/tasks/{id}` | Delete a task | 204 No Content |

### Request/Response Examples

#### Create a task

```http
POST /tasks
Content-Type: application/json

{
  "title": "Review pull request",
  "description": "Check authentication flow",
  "status": "Todo"
}
```

Response (201 Created):

```json
{
  "id": 1,
  "title": "Review pull request",
  "description": "Check authentication flow",
  "status": "Todo",
  "created_at": "2026-06-30T10:00:00Z",
  "updated_at": "2026-06-30T10:00:00Z"
}
```

#### Update a task (partial update supported)

```http
PUT /tasks/1
Content-Type: application/json

{
  "status": "In Progress"
}
```

Only the fields you send will be updated. Other fields remain unchanged.

### Validation Rules

| Field | Rules |
|-------|-------|
| `title` | Required, 1-200 characters |
| `description` | Optional, can be null |
| `status` | Must be one of: `Todo`, `In Progress`, `Done` |

### Error Responses

| Status | Description |
|--------|-------------|
| 404 Not Found | Task with given ID does not exist |
| 422 Unprocessable Entity | Validation failed (invalid input) |

## Project Structure

```
task-tracker/
├── backend/
│   ├── app/
│   │   ├── crud/
│   │   │   └── task.py           # Database operations
│   │   ├── models/
│   │   │   └── task.py           # SQLAlchemy ORM models
│   │   ├── routers/
│   │   │   └── task.py           # API endpoints
│   │   ├── schemas/
│   │   │   └── task.py           # Pydantic validation schemas
│   │   ├── database.py           # DB connection, session, get_db dependency
│   │   └── main.py               # FastAPI app entry point
│   ├── .env.example              # Environment variables template
│   ├── .gitignore
│   └── requirements.txt          # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   │   └── main.css          # Tailwind import
│   │   ├── components/
│   │   │   ├── TaskList.vue      # Main container, state management
│   │   │   ├── TaskForm.vue      # Create task form
│   │   │   └── TaskItem.vue      # Single task card with edit/delete
│   │   ├── services/
│   │   │   └── taskService.js    # Axios API client
│   │   ├── App.vue               # Root component
│   │   └── main.js               # Vue app entry point
│   ├── .env.example              # Environment variables template
│   ├── .gitignore
│   ├── index.html
│   ├── package.json              # Node dependencies
│   └── vite.config.js            # Vite + Tailwind config
│
└── README.md
```

> Note: Each Python package folder (`app/`, `crud/`, `models/`, `routers/`, `schemas/`) contains an `__init__.py` file (omitted from the tree for clarity).

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `your_password` |
| `DB_NAME` | Database name | `task_tracker` |

### Frontend (`frontend/.env`)

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API base URL | `http://127.0.0.1:8000` |

Note: All Vite environment variables must be prefixed with `VITE_` to be accessible in the browser.

## Design Decisions

This section explains the rationale behind key technical choices.

### Why FastAPI?

FastAPI was chosen over alternatives (Flask, Django REST) for:

- **Automatic data validation** via Pydantic type hints (no manual schema validation)
- **Auto-generated OpenAPI documentation** at `/docs` (Swagger UI)
- **Async-first architecture** via ASGI (better performance than WSGI Flask)
- **Modern Python idioms** (type hints, dependency injection)
- **Low boilerplate** compared to Django REST Framework

### Why SQLAlchemy ORM (instead of raw SQL)?

- **Database-agnostic** — easy to switch engines without rewriting queries
- **SQL injection protection** by default (parameterized queries)
- **Connection pooling** built-in
- **Type-safe** queries with Python objects
- `Base.metadata.create_all()` enables automatic table creation as required by the assessment

### Why separate `models/` and `schemas/`?

- **`models/`** (SQLAlchemy) defines the **database structure**
- **`schemas/`** (Pydantic) defines the **API contract**

These can diverge over time. For example, the database stores `created_at`, but the API request to create a task shouldn't include it (server-generated). Keeping them separate prevents leaky abstractions.

### Why a Repository/CRUD layer?

Separating HTTP handling (routers) from database operations (crud) provides:

- **Testability** — CRUD functions can be tested without HTTP overhead
- **Reusability** — same operations can be called from scheduled jobs, CLI tools, etc.
- **Single Responsibility Principle** — routers focus on HTTP, CRUD focuses on data

### Why VARCHAR + CheckConstraint instead of PostgreSQL ENUM for status?

Trade-off analysis:

| Aspect | PostgreSQL ENUM | VARCHAR + CHECK |
|---|---|---|
| Type safety | Strong | Strong (via CHECK) |
| Evolution (add/remove values) | Hard (requires migration) | Easy (update CHECK) |
| Cross-database portability | PostgreSQL-only | Portable |

VARCHAR + CHECK chosen for flexibility. The actual enforcement happens in three layers:
1. Pydantic `Literal` (application boundary)
2. Database CHECK constraint (defense in depth)
3. Client-side dropdown (UX)

### Why Vue 3 Composition API?

- **Better code organization** for complex components (logic grouped by feature, not by option type)
- **Type-inference friendly** for IDEs
- **Reusable composables** (similar to React hooks)
- **Modern standard** for new Vue 3 projects

### Why a Service Layer in the frontend?

`taskService.js` abstracts all API calls in one place. Components call `taskService.create()` instead of `axios.post('/tasks', ...)` directly.

Benefits:
- **Single source of truth** for API endpoints
- **Easy to mock** for testing
- **Centralized configuration** (base URL, headers, interceptors)
- **Refactoring safety** — API URL change requires editing one file

### Why no automated tests?

Automated tests were not implemented because they are outside the scope of the assessment. For production, I would add:

- **Backend:** `pytest` for CRUD functions, `httpx` for endpoint tests
- **Frontend:** `vitest` + `@vue/test-utils` for component tests, `Playwright` for E2E

## Potential Improvements

Features intentionally scoped out, but valuable for production:

- **Authentication & Authorization** (JWT, role-based access)
- **Database migrations** with Alembic (production-grade schema versioning)
- **Pagination** for large task lists
- **Filter and search** by status, date, keyword
- **Toast notifications** for user feedback
- **Centralized error handling** via Axios interceptors
- **Soft delete** with `deleted_at` timestamp instead of hard delete
- **Logging and monitoring** (structured logging, Sentry integration)
- **CI/CD pipeline** with GitHub Actions
- **TypeScript** for frontend type safety

## License

This project was created for technical assessment purposes.

## Author

Built by David Christian Nathaniel as part of an IT Developer Intern technical assessment at PT Global Loyalty Indonesia (Alfagift).