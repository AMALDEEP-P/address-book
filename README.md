# Address Book API

A **production-ready Address Book API** built with [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://docs.sqlalchemy.org/), [Alembic](https://alembic.sqlalchemy.org/), and [Loguru](https://loguru.readthedocs.io/).  
Supports user and address management, geospatial queries, async database access, and robust logging.

---

## Features

- **User Management**: Create, update, retrieve users.
- **Address Management**: Create, update (partial/patch), soft-delete, list addresses.
- **Geospatial Search**: List addresses within a given distance of coordinates (Haversine formula).
- **Async SQLAlchemy**: Fully async DB access for performance.
- **Alembic Migrations**: Versioned schema migrations.
- **Pydantic Validation**: Strict request/response validation.
- **Loguru Logging**: Production-grade, file and console logging.
- **Environment Config**: `.env` support for secrets and config.

---

## Project Structure

```
address_book/
├── app/
│   ├── address/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes.py
│   │   └── helpers.py
│   ├── user/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── routes.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── session.py
│   ├── logging/
│   │   ├── __init__.py
│   │   └── logging_config.py
│   └── __init__.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── ...
├── main.py
├── .env
├── pyproject.toml
└── README.md
```

---

## Quickstart

### 1. **Clone & Install**

```bash
git clone <repo-url>
cd address_book
poetry install
```

### 2. **Configure Environment**

Create a `.env` file:

```
DATABASE_URL=sqlite+aiosqlite:///address.db
LOG_LEVEL=INFO
LOG_FILE=app.log
PORT=8000
RELOAD=True
```

### 3. **Run Migrations**

```bash
poetry run alembic upgrade head
```

### 4. **Start the API**

```bash
poetry run python main.py
```

- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health check: [http://localhost:8000/ping](http://localhost:8000/ping)

---

## API Endpoints

### **User**

- `POST /user/` — Create user
- `PUT /user/{user_id}` — Update user
- `GET /user/{user_id}` — Get user

### **Address**

- `POST /address/` — Create address (no duplicate lat/lon)
- `PATCH /address/{address_id}` — Partial update address
- `DELETE /address/{address_id}` — Soft delete address
- `GET /address/` — List all addresses
- `GET /address/nearby/?latitude=...&longitude=...&distance_km=...` — Addresses within distance

---

## Logging

- Uses [Loguru](https://loguru.readthedocs.io/) for structured logging.
- Logs to both console and `app.log` (rotates at 10MB, keeps 10 days).
- Log level and file can be set via `.env`.

**Usage in code:**
```python
from loguru import logger
logger.info("Something happened")
logger.error("Something failed: {}", error)
```

---

## Development

- **Testing:**  
  Add tests in `tests/` and run with:
  ```bash
  poetry run pytest
  ```

- **Migrations:**  
  Create new migration:
  ```bash
  poetry run alembic revision --autogenerate -m "your message"
  poetry run alembic upgrade head
  ```

- **Formatting:**  
  Use [Black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/).

---

## Production

- Run with a production ASGI server (e.g. [gunicorn](https://www.uvicorn.org/deployment/#gunicorn)):
  ```bash
  poetry run gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
  ```

---

## Environment Variables

| Variable     | Description                        | Default                      |
|--------------|------------------------------------|------------------------------|
| DATABASE_URL | SQLAlchemy DB URL                  | sqlite+aiosqlite:///address.db |
| LOG_LEVEL    | Logging level                      | INFO                         |
| LOG_FILE     | Log file name                      | app.log                      |
| PORT         | API port                           | 8000                         |
| RELOAD       | Auto-reload on code changes        | False                        |

---

## License

MIT

---

## Authors

- Amaldeep <amalatl6@gmail.com>

---

## Contributing

Pull requests welcome! Please open an issue first to discuss changes.
