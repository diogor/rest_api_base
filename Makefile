include .env
export $(shell sed 's/=.*//' .env)

migrate:
	poetry run alembic upgrade head

start:
	poetry run uvicorn web.main:app --reload
