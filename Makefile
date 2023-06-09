include .env
export $(shell sed 's/=.*//' .env)

migrate:
	poetry run alembic upgrade head

migration:
	poetry run alembic revision --autogenerate -m "$(name)"

start:
	poetry run uvicorn web.main:app --reload
