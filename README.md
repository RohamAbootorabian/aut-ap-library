# Library Management System

A REST API for managing a library — books, users, and book reservations — built with Flask, plus a browser UI for working with it.

Written for the Advanced Programming course at Amirkabir University of Technology (Tehran Polytechnic).

```
GET  /api/v1/books                    →  list the catalogue
POST /api/v1/books/1/reserve          →  reserve a book  (header: user-id)
GET  /api/v1/users/1/reservations     →  what user 1 is holding
```

## Features

- **Books** — list, fetch, create and delete, with server-assigned ids
- **Users** — list, fetch, create, update and delete, with unique usernames
- **Reservations** — reserve and return a book, with a per-user reservation list
- **Validation** — required fields checked, duplicate usernames rejected, meaningful HTTP status codes on every path
- **Web UI** — a single-page frontend served by the same app, with live search over books and users
- **JSON persistence** — no database server to install; state lives in `db.json`
- **OpenAPI spec** — every endpoint described in `swagger.yaml`

## What I built

The course provided a skeleton: route signatures whose bodies returned empty
placeholders (`return jsonify({"books": []})`), the OpenAPI spec, the test
suite, and a seed `db.json`.

Everything that makes it work is mine — roughly 1,000 lines:

- **`database.py`** — the persistence layer, written from scratch: reading and writing `db.json`, creating it if absent, and surviving a missing or malformed file
- **Every endpoint body** — the CRUD logic, validation, reservation rules and error handling behind all 12 routes
- **The entire frontend** — `index.html`, `app.js` and `style.css`; the skeleton had no UI at all
- **`PUT /users/{id}`** — documented in the spec but never implemented, so I added it

## Getting started

Requires Python 3.13+.

**With [uv](https://github.com/astral-sh/uv):**

```bash
uv sync
uv run main.py
```

**With plain Python:**

```bash
pip install flask flask-cors
python3 main.py
```

Open **http://localhost:8080** for the web UI, or call the API directly at
`http://localhost:8080/api/v1`.

To run on a different port:

```bash
python3 -c "from app import app; app.run(port=5001)"
```

## Project structure

```
main.py                  entry point
database.py              persistence layer over db.json
db.json                  seed data (2 users, 3 books)
swagger.yaml             OpenAPI 3.0 specification
app/
  application.py         Flask app, CORS, static file serving
  routes/
    books.py             book endpoints
    users.py             user endpoints
    reservation.py       reserve / return / list reservations
  static/
    index.html           web UI
    js/app.js            frontend logic
    css/style.css        styling
tests/
  test_books.py
  test_users.py
  test_reservations.py
```

Routes are separated from data access, so the storage layer could be swapped
for a real database without touching the endpoint code.

## API reference

Base URL: `http://localhost:8080/api/v1`

### Books

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/books` | List all books |
| `GET` | `/books/{id}` | Get one book |
| `POST` | `/books` | Create a book — requires `title`, `author`, `isbn` |
| `DELETE` | `/books/{id}` | Delete a book |

### Users

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/users` | List all users |
| `GET` | `/users/{id}` | Get one user |
| `POST` | `/users` | Create a user — requires `username`, `name`, `email` |
| `PUT` | `/users/{id}` | Update a user |
| `DELETE` | `/users/{id}` | Delete a user |

### Reservations

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/books/{id}/reserve` | Reserve a book |
| `DELETE` | `/books/{id}/reserve` | Return a book |
| `GET` | `/users/{id}/reservations` | List a user's reservations |

Reservation endpoints identify the caller with a **`user-id` request header**.

> Send it as `user-id`, not `user_id`. Headers containing underscores are
> dropped in transit by many servers and proxies, so the underscored spelling
> arrives as no header at all and the request is rejected with a 400.

Ids are assigned by the server on create — clients do not supply them.

### Example

```bash
# reserve a book
curl -X POST -H "user-id: 1" http://localhost:8080/api/v1/books/1/reserve

# see what that user is holding
curl -H "user-id: 1" http://localhost:8080/api/v1/users/1/reservations

# return it
curl -X DELETE -H "user-id: 1" http://localhost:8080/api/v1/books/1/reserve
```

### Status codes

| Code | Meaning |
|---|---|
| `200` | Success |
| `201` | Created |
| `400` | Missing or invalid fields, duplicate username, book already reserved |
| `403` | Requesting another user's reservations |
| `404` | Book or user not found |
| `500` | Could not read the data file |

## Web UI

The frontend is served from the same Flask app at `/`, so there is nothing
separate to start. It covers:

- Browsing books with availability status, and reserving or returning them
- Adding and deleting books
- Adding and editing users, with their live reservation count
- Viewing a user's reservations
- **Search** across both tables, filtering as you type over every visible field
- Section state kept in the URL hash, so a refresh stays where you were

API calls use a relative path, so the UI works on whatever port the app is
running on.

## Tests

```bash
uv run pytest            # or: python3 -m pytest tests/ -v
```

## Data storage

State is a single `db.json` file, resolved next to `database.py` — so the app
runs from any working directory, on any machine. Override the location with
the `DB_PATH` environment variable:

```bash
DB_PATH=/tmp/library.json python3 main.py
```

This keeps the project dependency-free to run, at the cost of concurrent-write
safety. Moving to SQLite or Postgres would mean rewriting `database.py` and
nothing else.

## Known limitations

- JSON file storage is not safe under concurrent writes
- No authentication — the `user-id` header is trusted as sent
- Reservations have no due dates or history
