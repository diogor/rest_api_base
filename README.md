# REST Api Base

## Features

- ORM (sqlmodel)
- Migrations (alembic)
- Authentication (JWT)

## Requirements

- Poetry (https://python-poetry.org/)
- Make (optional)

## Setup and install

- Copy `.env.example` -> `.env` and edit according to your needs
- Run `poetry install`

## Migrations

- Update your database: `make migrate` or `poetry run alembic upgrade head`
- Create new migration:
  - Create or edit your models at `models/`
    - If you are creating a new model, make sure to add it to `models/__init__.py`
  - `make migration name="migration name"` or `poetry run alembic revision --autogenerate -m "migration name"`
    - This will create a new migration file in `migrations/versions/`
  - Review the generated migration file and make any necessary adjustments
- Apply migrations: `make migrate` or `poetry run alembic upgrade head`

## Start development server

- `make start`

## Documentation

Go to `/docs` to access swagger auto-generated docs.
