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
- Create new migration: `make migration name="migration name"`

## Start development server

- `make start`

## Documentation

Go to `/docs` to access swagger auto-generated docs.
